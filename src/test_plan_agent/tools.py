"""Ferramentas controladas para apoio ao agente."""


def prepare_minimal_context(user_story: str) -> dict[str, str]:
    """Prepara um contexto local mínimo sem acessar recursos externos."""
    normalized_story = " ".join(user_story.strip().split())

    return {
        "source": "entrada_do_usuario",
        "summary": normalized_story[:160],
        "next_step": "expandir contexto local em etapas futuras",
    }