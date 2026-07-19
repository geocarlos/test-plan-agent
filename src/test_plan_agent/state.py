"""Estado compartilhado do fluxo LangGraph."""

from collections.abc import Callable
from typing import Any, TypedDict


ProgressCallback = Callable[[str], None]


class AgentState(TypedDict, total=False):
    """Representa os dados trafegados entre os nós do agente."""

    user_story: str
    validation_errors: list[str]
    local_context: dict[str, Any]
    story_analysis: dict[str, Any]
    acceptance_criteria: list[str]
    test_scenarios: list[dict[str, Any]]
    edge_cases: list[str]
    example_data: list[str]
    ambiguity_risks: list[str]
    automation_suggestions: list[str]
    final_answer: str
    generation_mode: str
    fallback_used: bool
    llm_provider: str
    llm_model: str
    provisional_response: dict[str, Any]
    _progress_callback: ProgressCallback


def create_initial_state(user_story: str) -> AgentState:
    """Cria um estado inicial previsível para execução do grafo."""
    return {
        "user_story": user_story,
        "validation_errors": [],
        "local_context": {},
        "story_analysis": {},
        "acceptance_criteria": [],
        "test_scenarios": [],
        "edge_cases": [],
        "example_data": [],
        "ambiguity_risks": [],
        "automation_suggestions": [],
        "final_answer": "",
        "generation_mode": "",
        "fallback_used": False,
        "llm_provider": "",
        "llm_model": "",
        "provisional_response": {},
    }