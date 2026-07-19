from argparse import Namespace

import pytest

from test_plan_agent import __version__
from test_plan_agent.cli import DEFAULT_USER_STORY, main, read_user_stories_file, read_user_story_file, resolve_user_stories, resolve_user_story
from test_plan_agent.graph import run_agent
from test_plan_agent.llm import LLMConfigurationError, LLMGenerationError
from test_plan_agent.state import create_initial_state
from test_plan_agent.tools import LocalFileReadError, read_local_data_file
from test_plan_agent.validators import detect_ambiguous_terms, validate_user_story


MAIN_MARKDOWN_SECTIONS = [
    "# Plano de Testes",
    "## Resumo da história",
    "## Lacunas e ambiguidades",
    "## Critérios de aceite verificáveis",
    "## Cenários principais em Given/When/Then",
    "## Cenários alternativos e negativos",
    "## Casos de borda",
    "## Dados de exemplo",
    "## Sugestões de automação",
    "## Riscos e observações",
]


@pytest.fixture(autouse=True)
def clear_llm_environment(monkeypatch) -> None:
    for variable in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_BASE_URL"):
        monkeypatch.setenv(variable, "")


def test_package_version() -> None:
    assert __version__ == "0.1.0"


def test_create_initial_state() -> None:
    state = create_initial_state("Como usuário, quero acessar meu histórico de pedidos.")

    assert state["user_story"] == "Como usuário, quero acessar meu histórico de pedidos."
    assert state["validation_errors"] == []
    assert state["local_context"] == {}
    assert state["story_analysis"] == {}
    assert state["acceptance_criteria"] == []
    assert state["test_scenarios"] == []
    assert state["edge_cases"] == []
    assert state["example_data"] == []
    assert state["ambiguity_risks"] == []
    assert state["automation_suggestions"] == []
    assert state["final_answer"] == ""
    assert state["generation_mode"] == ""
    assert state["fallback_used"] is False
    assert state["llm_provider"] == ""
    assert state["llm_model"] == ""
    assert state["provisional_response"] == {}


def test_resolve_user_story_uses_default_when_no_input() -> None:
    args = Namespace(user_story=None, story_file=None)

    assert resolve_user_story(args) == DEFAULT_USER_STORY


def test_read_user_story_file_reads_markdown(tmp_path) -> None:
    story_file = tmp_path / "historia.md"
    story_file.write_text(
        "# História válida\n\nComo cliente, quero consultar pedidos recentes para acompanhar entregas.\n",
        encoding="utf-8",
    )

    assert read_user_story_file(str(story_file)) == "Como cliente, quero consultar pedidos recentes para acompanhar entregas."


def test_read_user_stories_file_splits_markdown_sections(tmp_path) -> None:
    story_file = tmp_path / "historias.md"
    story_file.write_text(
        """## Histórias de Usuário para CRM

### 1. Cadastro de Leads
- **Como** representante de vendas,
- **Quero** registrar novos leads,
- **Para que** eu possa acompanhar o progresso no funil.

---

### 2. Atualização de Status
- **Como** gerente comercial,
- **Quero** atualizar o status de cada oportunidade,
- **Para que** eu tenha visibilidade clara do pipeline.
""",
        encoding="utf-8",
    )

    assert read_user_stories_file(str(story_file)) == [
        "Como representante de vendas, Quero registrar novos leads, Para que eu possa acompanhar o progresso no funil.",
        "Como gerente comercial, Quero atualizar o status de cada oportunidade, Para que eu tenha visibilidade clara do pipeline.",
    ]


def test_resolve_user_stories_uses_file_sections(tmp_path) -> None:
    story_file = tmp_path / "historias.md"
    story_file.write_text(
        "Como cliente, quero consultar pedidos para acompanhar entregas.\n\n---\n\nComo gestor, quero ver métricas para acompanhar resultados.",
        encoding="utf-8",
    )
    args = Namespace(user_story=None, story_file=str(story_file))

    assert resolve_user_stories(args) == [
        "Como cliente, quero consultar pedidos para acompanhar entregas.",
        "Como gestor, quero ver métricas para acompanhar resultados.",
    ]


def test_main_generates_one_plan_per_story_from_markdown_file(tmp_path, monkeypatch, capsys) -> None:
    story_file = tmp_path / "historias.md"
    story_file.write_text(
        """# Histórias

### 1. Cadastro
Como representante de vendas, quero registrar novos leads para acompanhar oportunidades.

---

### 2. Relatórios
Como diretor de vendas, quero gerar relatórios semanais para avaliar a performance da equipe.
""",
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["test-plan-agent", "--file", str(story_file)])

    main()

    output = capsys.readouterr().out
    assert output.count("# Plano de Testes") == 2
    assert "## História 1" in output
    assert "## História 2" in output
    assert "Como representante de vendas" in output
    assert "Como diretor de vendas" in output


def test_read_user_story_file_rejects_non_markdown(tmp_path) -> None:
    story_file = tmp_path / "historia.txt"
    story_file.write_text("Como cliente, quero consultar pedidos recentes.", encoding="utf-8")

    try:
        read_user_story_file(str(story_file))
    except ValueError as error:
        assert str(error) == "Informe um arquivo Markdown com extensão .md ou .markdown."
    else:
        raise AssertionError("A leitura deveria falhar para arquivo que não é Markdown.")


def test_resolve_user_story_rejects_argument_and_file() -> None:
    args = Namespace(user_story="Como cliente, quero consultar pedidos.", story_file="historia.md")

    try:
        resolve_user_story(args)
    except ValueError as error:
        assert str(error) == "Use uma história no argumento ou --file, não ambos."
    else:
        raise AssertionError("A resolução deveria falhar com argumento e arquivo juntos.")


def test_validate_user_story_requires_content() -> None:
    assert validate_user_story("   ") == [
        "Informe uma história de usuário, issue ou requisito funcional."
    ]


def test_validate_user_story_requires_minimum_length() -> None:
    assert validate_user_story("curta") == [
        "A entrada deve ter pelo menos 20 caracteres para análise inicial."
    ]


def test_validate_user_story_reports_missing_basic_parts() -> None:
    assert validate_user_story("O relatório mensal precisa ser exportado") == [
        "A história deve indicar o ator ou perfil envolvido.",
        "A história deve indicar o resultado esperado ou valor gerado.",
    ]


def test_validate_user_story_reports_missing_actor() -> None:
    assert validate_user_story("Quero exportar relatórios mensais para acompanhar indicadores.") == [
        "A história deve indicar o ator ou perfil envolvido."
    ]


def test_validate_user_story_reports_missing_goal() -> None:
    assert validate_user_story("Como cliente autenticado, para acompanhar meus pedidos recentes.") == [
        "A história deve indicar o objetivo ou ação esperada."
    ]


def test_validate_user_story_reports_missing_expected_result() -> None:
    assert validate_user_story("Como gestor, quero aprovar solicitações pendentes.") == [
        "A história deve indicar o resultado esperado ou valor gerado."
    ]


def test_detect_ambiguous_terms() -> None:
    assert detect_ambiguous_terms("Como usuário, quero um fluxo rápido, simples e completo para finalizar compra.") == [
        "rápido",
        "simples",
        "completo",
    ]


def test_run_agent_returns_structured_test_plan() -> None:
    final_state = run_agent(
        "Como cliente autenticado, quero consultar meus pedidos recentes para acompanhar a entrega."
    )

    assert final_state["validation_errors"] == []
    assert final_state["local_context"]["source"] == "data/test_templates.md"
    assert "Critérios de Aceite" in final_state["local_context"]["template_reference"]
    assert final_state["provisional_response"]["status"] == "ready"
    assert final_state["generation_mode"] == "deterministic_fallback"
    assert final_state["fallback_used"] is True
    assert final_state["acceptance_criteria"]
    assert final_state["test_scenarios"]
    assert "fallback determinístico usado" in final_state["final_answer"]
    assert "# Plano de Testes" in final_state["final_answer"]
    assert "## Critérios de aceite verificáveis" in final_state["final_answer"]
    assert "## Cenários principais em Given/When/Then" in final_state["final_answer"]
    assert "Contexto local usado: data/test_templates.md" in final_state["final_answer"]


def test_run_agent_reports_progress_with_callback() -> None:
    progress_messages: list[str] = []

    final_state = run_agent(
        "Como cliente autenticado, quero consultar meus pedidos recentes para acompanhar a entrega.",
        progress_callback=progress_messages.append,
    )

    assert final_state["generation_mode"] == "deterministic_fallback"
    assert "_progress_callback" not in final_state
    assert progress_messages[0] == "Validando entrada..."
    assert "Preparando contexto local..." in progress_messages
    assert "Nenhuma configuração de LLM encontrada; usando fallback determinístico..." in progress_messages


def test_run_agent_completes_full_flow_for_valid_story() -> None:
    final_state = run_agent(
        "Como analista financeiro, quero exportar transações filtradas para reconciliar pagamentos."
    )

    assert final_state["provisional_response"]["status"] == "ready"
    assert final_state["story_analysis"]["summary"].startswith("Como analista financeiro")
    assert len(final_state["acceptance_criteria"]) == 3
    assert len(final_state["test_scenarios"]) == 3
    assert len(final_state["edge_cases"]) == 4
    assert len(final_state["example_data"]) == 4
    assert len(final_state["automation_suggestions"]) == 4


def test_run_agent_final_answer_contains_main_sections() -> None:
    final_state = run_agent(
        "Como administrador, quero bloquear acessos suspeitos para proteger contas de clientes."
    )

    for section in MAIN_MARKDOWN_SECTIONS:
        assert section in final_state["final_answer"]


def test_run_agent_keeps_using_local_template_context() -> None:
    final_state = run_agent(
        "Como cliente, quero consultar o histórico de faturas para conferir cobranças anteriores."
    )

    assert final_state["local_context"]["source"] == "data/test_templates.md"
    assert final_state["local_context"]["summary"] == final_state["user_story"]
    assert final_state["local_context"]["template_size_bytes"] > 0
    assert "Checklist de Testabilidade" in final_state["local_context"]["template_reference"]
    assert final_state["provisional_response"]["local_template_source"] == "data/test_templates.md"


def test_run_agent_uses_llm_when_configuration_exists(monkeypatch) -> None:
    captured_messages = []
    progress_messages: list[str] = []

    class FakeChatModel:
        def invoke(self, messages):
            captured_messages.extend(messages)
            return type("FakeResponse", (), {"content": "# Plano de Testes\n\n## Resumo da história\nGerado por LLM mockado."})()

    monkeypatch.setenv("OPENAI_API_KEY", "chave-falsa-para-teste")
    monkeypatch.setenv("OPENAI_MODEL", "modelo-falso")
    monkeypatch.setattr("test_plan_agent.llm._build_chat_model", lambda config: FakeChatModel())

    final_state = run_agent(
        "Como cliente autenticado, quero consultar meus pedidos recentes para acompanhar a entrega.",
        progress_callback=progress_messages.append,
    )

    assert final_state["generation_mode"] == "llm"
    assert final_state["fallback_used"] is False
    assert final_state["llm_provider"] == "openai"
    assert final_state["llm_model"] == "modelo-falso"
    assert final_state["provisional_response"]["message"] == "Plano de testes gerado com LLM."
    assert final_state["final_answer"] == "# Plano de Testes\n\n## Resumo da história\nGerado por LLM mockado."
    assert captured_messages[0][0] == "system"
    assert captured_messages[1][0] == "human"
    assert "data/test_templates.md" in captured_messages[1][1]
    assert "Critérios de Aceite" in captured_messages[1][1]
    assert "LLM configurado; enviando solicitação ao provedor..." in progress_messages
    assert "Aguardando resposta do LLM..." in progress_messages
    assert "Plano concluído com LLM." in progress_messages


def test_main_prints_progress_to_stderr_without_polluting_markdown(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["test-plan-agent", "Como cliente autenticado, quero consultar meus pedidos recentes para acompanhar a entrega."],
    )

    main()

    captured = capsys.readouterr()
    assert captured.out.startswith("**Aviso:** fallback determinístico usado")
    assert "[Test-Plan Agent]" not in captured.out
    assert "[Test-Plan Agent] Processando história 1/1..." in captured.err
    assert "[Test-Plan Agent] Preparando contexto local..." in captured.err


def test_run_agent_fails_when_llm_variable_exists_without_api_key(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "modelo-configurado-sem-chave")

    with pytest.raises(LLMConfigurationError) as error:
        run_agent("Como gestor, quero visualizar métricas para acompanhar resultados.")

    assert "Configuração de LLM incompleta" in str(error.value)
    assert "fallback determinístico" in str(error.value)


def test_run_agent_does_not_fallback_on_provider_auth_error(monkeypatch) -> None:
    class FakeAuthenticationError(Exception):
        status_code = 401

    class FakeChatModel:
        def invoke(self, messages):
            raise FakeAuthenticationError("invalid api key")

    monkeypatch.setenv("OPENAI_API_KEY", "chave-falsa-para-teste")
    monkeypatch.setattr("test_plan_agent.llm._build_chat_model", lambda config: FakeChatModel())

    with pytest.raises(LLMGenerationError) as error:
        run_agent("Como cliente, quero consultar faturas para conferir cobranças.")

    assert "Falha de autenticação ou autorização" in str(error.value)
    assert "fallback determinístico não foi usado" in str(error.value)


def test_main_reports_llm_error_as_controlled_exit(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "modelo-configurado-sem-chave")
    monkeypatch.setattr(
        "sys.argv",
        ["test-plan-agent", "Como gestor, quero visualizar métricas para acompanhar resultados."],
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert "Configuração de LLM incompleta" in str(error.value.code)


def test_run_agent_reports_invalid_short_story() -> None:
    final_state = run_agent("curta")

    assert final_state["validation_errors"] == [
        "A entrada deve ter pelo menos 20 caracteres para análise inicial."
    ]
    assert final_state["provisional_response"]["status"] == "invalid"
    assert "Lacuna: A entrada deve ter pelo menos 20 caracteres" in final_state["final_answer"]


def test_run_agent_reports_incomplete_story_gaps() -> None:
    final_state = run_agent("A exportação de relatórios precisa ser liberada")

    assert final_state["provisional_response"]["status"] == "invalid"
    assert "A história deve indicar o ator ou perfil envolvido." in final_state["validation_errors"]
    assert "A história deve indicar o resultado esperado ou valor gerado." in final_state["validation_errors"]
    assert "Lacuna: A história deve indicar o ator ou perfil envolvido." in final_state["final_answer"]


def test_run_agent_reports_ambiguous_terms() -> None:
    final_state = run_agent(
        "Como cliente, quero uma busca rápida e intuitiva para encontrar pedidos."
    )

    assert "rápido" in final_state["story_analysis"]["ambiguous_terms"]
    assert "intuitivo" in final_state["story_analysis"]["ambiguous_terms"]
    assert "Termo ambíguo: 'rápido'" in final_state["final_answer"]


def test_read_local_data_file_returns_allowed_template() -> None:
    result = read_local_data_file("test_templates.md")

    assert result["source"] == "data/test_templates.md"
    assert "Checklist de Testabilidade" in result["content"]


def test_read_local_data_file_rejects_missing_file() -> None:
    try:
        read_local_data_file("arquivo-inexistente.md")
    except LocalFileReadError as error:
        assert str(error) == "Arquivo não encontrado na base local."
    else:
        raise AssertionError("A leitura deveria falhar para arquivo inexistente.")


def test_read_local_data_file_rejects_invalid_extension() -> None:
    try:
        read_local_data_file("test_templates.json")
    except LocalFileReadError as error:
        assert str(error) == "Extensão inválida: use apenas arquivos .md ou .txt."
    else:
        raise AssertionError("A leitura deveria falhar para extensão inválida.")


def test_read_local_data_file_rejects_path_traversal() -> None:
    try:
        read_local_data_file("../README.md")
    except LocalFileReadError as error:
        assert str(error) == "Acesso negado: o arquivo deve estar dentro da pasta data/."
    else:
        raise AssertionError("A leitura deveria falhar para tentativa fora de data/.")


def test_read_local_data_file_rejects_large_file(tmp_path, monkeypatch) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    large_file = data_dir / "grande.md"
    large_file.write_text("conteúdo acima do limite", encoding="utf-8")
    monkeypatch.setattr("test_plan_agent.tools.DATA_DIR", data_dir)
    monkeypatch.setattr("test_plan_agent.tools.MAX_FILE_SIZE_BYTES", 5)

    try:
        read_local_data_file("grande.md")
    except LocalFileReadError as error:
        assert str(error) == "Arquivo grande demais para leitura controlada."
    else:
        raise AssertionError("A leitura deveria falhar para arquivo grande demais.")