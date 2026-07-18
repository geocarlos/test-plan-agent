"""Grafo mínimo do Test-Plan Agent com LangGraph."""

from langgraph.graph import END, START, StateGraph

from test_plan_agent.state import AgentState
from test_plan_agent.tools import prepare_minimal_context
from test_plan_agent.validators import validate_user_story


def validate_input(state: AgentState) -> AgentState:
    """Nó responsável por validar a entrada principal."""
    return {"validation_errors": validate_user_story(state.get("user_story", ""))}


def prepare_context(state: AgentState) -> AgentState:
    """Nó responsável por preparar contexto mínimo controlado."""
    return {"local_context": prepare_minimal_context(state.get("user_story", ""))}


def generate_provisional_response(state: AgentState) -> AgentState:
    """Nó responsável por gerar uma resposta estruturada provisória."""
    validation_errors = state.get("validation_errors", [])
    status = "invalid" if validation_errors else "ready"

    return {
        "provisional_response": {
            "status": status,
            "message": "Fluxo mínimo do agente executado com sucesso.",
            "validation_errors": validation_errors,
            "prepared_context": state.get("local_context", {}),
            "planned_sections": [
                "critérios de aceite",
                "cenários Given/When/Then",
                "casos negativos",
                "casos de borda",
                "dados de exemplo",
                "riscos de ambiguidade",
                "sugestões de automação",
            ],
        }
    }


def build_graph():
    """Constrói e compila o grafo mínimo do agente."""
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("validate_input", validate_input)
    graph_builder.add_node("prepare_context", prepare_context)
    graph_builder.add_node("generate_provisional_response", generate_provisional_response)

    graph_builder.add_edge(START, "validate_input")
    graph_builder.add_edge("validate_input", "prepare_context")
    graph_builder.add_edge("prepare_context", "generate_provisional_response")
    graph_builder.add_edge("generate_provisional_response", END)

    return graph_builder.compile()


def run_agent(user_story: str) -> AgentState:
    """Executa o grafo mínimo a partir de uma história de usuário."""
    graph = build_graph()
    return graph.invoke({"user_story": user_story})