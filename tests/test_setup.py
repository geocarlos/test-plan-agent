from test_plan_agent import __version__
from test_plan_agent.graph import run_agent
from test_plan_agent.state import create_initial_state
from test_plan_agent.validators import validate_user_story


def test_package_version() -> None:
    assert __version__ == "0.1.0"


def test_create_initial_state() -> None:
    state = create_initial_state("Como usuário, quero acessar meu histórico de pedidos.")

    assert state["user_story"] == "Como usuário, quero acessar meu histórico de pedidos."
    assert state["validation_errors"] == []
    assert state["local_context"] == {}
    assert state["provisional_response"] == {}


def test_validate_user_story_requires_content() -> None:
    assert validate_user_story("   ") == [
        "Informe uma história de usuário, issue ou requisito funcional."
    ]


def test_validate_user_story_requires_minimum_length() -> None:
    assert validate_user_story("curta") == [
        "A entrada deve ter pelo menos 20 caracteres para análise inicial."
    ]


def test_run_agent_returns_minimal_provisional_response() -> None:
    final_state = run_agent(
        "Como cliente autenticado, quero consultar meus pedidos recentes para acompanhar a entrega."
    )

    assert final_state["validation_errors"] == []
    assert final_state["local_context"]["source"] == "entrada_do_usuario"
    assert final_state["provisional_response"]["status"] == "ready"
    assert "cenários Given/When/Then" in final_state["provisional_response"]["planned_sections"]