"""Validações básicas para entradas do agente."""

import re


MINIMUM_USER_STORY_LENGTH = 20
AMBIGUOUS_TERMS = ("rápido", "simples", "intuitivo", "adequado", "melhor", "completo")
AMBIGUOUS_TERM_PATTERNS = {
    "rápido": r"\brápid[oa]s?\b",
    "simples": r"\bsimples\b",
    "intuitivo": r"\bintuitiv[oa]s?\b",
    "adequado": r"\badequad[oa]s?\b",
    "melhor": r"\bmelhores?\b",
    "completo": r"\bcomplet[oa]s?\b",
}


def detect_ambiguous_terms(user_story: str) -> list[str]:
    """Retorna termos subjetivos que precisam de definição objetiva."""
    normalized_story = user_story.casefold()
    return [term for term in AMBIGUOUS_TERMS if re.search(AMBIGUOUS_TERM_PATTERNS[term], normalized_story)]


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

    normalized_lower = normalized_story.casefold()

    if not re.search(r"\bcomo\b|\busuário\b|\busuario\b|\bcliente\b|\badministrador\b|\bgestor\b|\banalista\b|\bsistema\b", normalized_lower):
        errors.append("A história deve indicar o ator ou perfil envolvido.")

    if not re.search(r"\bquero\b|\bprecis[oa]\b|\bdevo\b|\bnecessito\b|\bpode\b|\bdeve\b", normalized_lower):
        errors.append("A história deve indicar o objetivo ou ação esperada.")

    if not re.search(r"\bpara\b|\ba fim de\b|\bde modo que\b|\bcom o objetivo de\b", normalized_lower):
        errors.append("A história deve indicar o resultado esperado ou valor gerado.")

    return errors