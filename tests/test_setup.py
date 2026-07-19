from test_plan_agent import __version__
from test_plan_agent.graph import run_agent
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
    assert state["provisional_response"] == {}


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
    assert final_state["acceptance_criteria"]
    assert final_state["test_scenarios"]
    assert "# Plano de Testes" in final_state["final_answer"]
    assert "## Critérios de aceite verificáveis" in final_state["final_answer"]
    assert "## Cenários principais em Given/When/Then" in final_state["final_answer"]
    assert "Contexto local usado: data/test_templates.md" in final_state["final_answer"]


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