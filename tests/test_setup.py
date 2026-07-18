from test_plan_agent import __version__
from test_plan_agent.graph import run_agent
from test_plan_agent.state import create_initial_state
from test_plan_agent.tools import LocalFileReadError, read_local_data_file
from test_plan_agent.validators import detect_ambiguous_terms, validate_user_story


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


def test_run_agent_reports_invalid_short_story() -> None:
    final_state = run_agent("curta")

    assert final_state["validation_errors"] == [
        "A entrada deve ter pelo menos 20 caracteres para análise inicial."
    ]
    assert final_state["provisional_response"]["status"] == "invalid"
    assert "Lacuna: A entrada deve ter pelo menos 20 caracteres" in final_state["final_answer"]


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