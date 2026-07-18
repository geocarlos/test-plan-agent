"""Estado compartilhado do fluxo LangGraph."""

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """Representa os dados trafegados entre os nós do agente."""

    user_story: str
    validation_errors: list[str]
    local_context: dict[str, Any]
    provisional_response: dict[str, Any]


def create_initial_state(user_story: str) -> AgentState:
    """Cria um estado inicial previsível para execução do grafo."""
    return {
        "user_story": user_story,
        "validation_errors": [],
        "local_context": {},
        "provisional_response": {},
    }