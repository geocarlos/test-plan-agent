"""Validações básicas para entradas do agente."""


MINIMUM_USER_STORY_LENGTH = 20


def validate_user_story(user_story: str) -> list[str]:
    """Valida a história de usuário informada e retorna erros encontrados."""
    errors: list[str] = []
    normalized_story = user_story.strip()

    if not normalized_story:
        errors.append("Informe uma história de usuário, issue ou requisito funcional.")
        return errors

    if len(normalized_story) < MINIMUM_USER_STORY_LENGTH:
        errors.append("A entrada deve ter pelo menos 20 caracteres para análise inicial.")

    return errors