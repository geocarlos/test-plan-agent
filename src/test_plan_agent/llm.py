"""Integração segura com LLM para geração do plano de testes."""

from dataclasses import dataclass
from os import getenv
from typing import Any

from dotenv import load_dotenv

from test_plan_agent.prompts import LLM_TEST_PLAN_PROMPT, PLAN_GENERATION_SYSTEM_PROMPT


DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
LLM_ENVIRONMENT_VARIABLES = ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_BASE_URL")


class LLMError(RuntimeError):
    """Erro controlado para falhas relacionadas ao LLM."""


class LLMConfigurationError(LLMError):
    """Erro controlado para configuração ausente ou incorreta de LLM."""


class LLMGenerationError(LLMError):
    """Erro controlado para falhas retornadas pelo provedor de LLM."""


@dataclass(frozen=True)
class LLMConfig:
    """Configuração mínima para chamada ao provedor de LLM."""

    provider: str
    model: str
    base_url: str | None = None


def _read_env(name: str) -> str:
    return (getenv(name) or "").strip()


def get_llm_config() -> LLMConfig | None:
    """Detecta configuração de LLM disponível sem expor valores sensíveis."""
    load_dotenv()

    configured_values = {name: _read_env(name) for name in LLM_ENVIRONMENT_VARIABLES}
    has_any_llm_setting = any(configured_values.values())

    if not has_any_llm_setting:
        return None

    if not configured_values["OPENAI_API_KEY"]:
        raise LLMConfigurationError(
            "Configuração de LLM incompleta: defina OPENAI_API_KEY ou remova as variáveis de LLM para usar o fallback determinístico."
        )

    return LLMConfig(
        provider="openai",
        model=configured_values["OPENAI_MODEL"] or DEFAULT_OPENAI_MODEL,
        base_url=configured_values["OPENAI_BASE_URL"] or None,
    )


def build_llm_prompt(state: dict[str, Any], deterministic_draft: str) -> str:
    """Monta o prompt humano enviado ao LLM com contexto local controlado."""
    local_context = state.get("local_context", {})
    story_analysis = state.get("story_analysis", {})

    return LLM_TEST_PLAN_PROMPT.format(
        user_story=state.get("user_story", ""),
        story_summary=story_analysis.get("summary", ""),
        validation_errors="\n".join(f"- {error}" for error in state.get("validation_errors", [])) or "- Nenhuma lacuna básica detectada.",
        local_context_source=local_context.get("source", "data/test_templates.md"),
        local_context=local_context.get("template_reference", ""),
        deterministic_draft=deterministic_draft,
    )


def _build_chat_model(config: LLMConfig):
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as error:
        raise LLMConfigurationError(
            "Configuração de LLM detectada, mas a dependência langchain-openai não está instalada. Execute uv sync."
        ) from error

    kwargs: dict[str, Any] = {
        "model": config.model,
        "temperature": 0.2,
    }
    if config.base_url:
        kwargs["base_url"] = config.base_url

    return ChatOpenAI(**kwargs)


def _extract_response_text(response: Any) -> str:
    content = getattr(response, "content", response)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts).strip()

    return str(content).strip()


def _controlled_provider_error(error: Exception) -> LLMGenerationError:
    error_name = error.__class__.__name__.lower()
    status_code = getattr(error, "status_code", None)

    if status_code in {401, 403} or any(term in error_name for term in ("auth", "permission", "forbidden")):
        return LLMGenerationError(
            "Falha de autenticação ou autorização no provedor de LLM. Verifique credenciais e permissões; o fallback determinístico não foi usado."
        )

    if status_code == 404 or any(term in error_name for term in ("notfound", "model")):
        return LLMGenerationError(
            "Modelo de LLM não encontrado ou indisponível. Verifique OPENAI_MODEL; o fallback determinístico não foi usado."
        )

    return LLMGenerationError(
        "Falha ao gerar plano com LLM. Verifique a configuração do provedor; o fallback determinístico não foi usado."
    )


def generate_plan_with_llm(state: dict[str, Any], deterministic_draft: str) -> tuple[str, dict[str, Any]]:
    """Gera o plano final com LLM quando houver configuração válida."""
    config = get_llm_config()
    if config is None:
        raise LLMConfigurationError("Nenhuma configuração de LLM disponível para geração.")

    chat_model = _build_chat_model(config)
    messages = [
        ("system", PLAN_GENERATION_SYSTEM_PROMPT),
        ("human", build_llm_prompt(state, deterministic_draft)),
    ]

    try:
        response = chat_model.invoke(messages)
    except Exception as error:
        raise _controlled_provider_error(error) from error

    final_answer = _extract_response_text(response)
    if not final_answer:
        raise LLMGenerationError(
            "O provedor de LLM retornou uma resposta vazia. O fallback determinístico não foi usado."
        )

    return final_answer, {
        "generation_mode": "llm",
        "fallback_used": False,
        "llm_provider": config.provider,
        "llm_model": config.model,
    }