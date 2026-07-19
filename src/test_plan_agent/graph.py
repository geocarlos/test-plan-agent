"""Grafo do Test-Plan Agent com geração estruturada de plano de testes."""

from langgraph.graph import END, START, StateGraph

from test_plan_agent.llm import LLMError, generate_plan_with_llm, get_llm_config
from test_plan_agent.prompts import (
    ACCEPTANCE_CRITERIA_PROMPT,
    FINAL_MARKDOWN_PROMPT,
    PLAN_GENERATION_SYSTEM_PROMPT,
    SCENARIO_GENERATION_PROMPT,
)
from test_plan_agent.state import AgentState, create_initial_state
from test_plan_agent.tools import prepare_minimal_context
from test_plan_agent.validators import detect_ambiguous_terms, validate_user_story


def _report_progress(state: AgentState, message: str) -> None:
    progress_callback = state.get("_progress_callback")
    if callable(progress_callback):
        progress_callback(message)


def validate_input(state: AgentState) -> AgentState:
    """Nó responsável por validar a entrada principal."""
    _report_progress(state, "Validando entrada...")
    return {"validation_errors": validate_user_story(state.get("user_story", ""))}


def route_after_validation(state: AgentState) -> str:
    """Define se a história pode seguir para geração do plano."""
    if state.get("validation_errors"):
        return "format_final_answer"

    return "prepare_context"


def prepare_context(state: AgentState) -> AgentState:
    """Nó responsável por preparar contexto mínimo controlado."""
    _report_progress(state, "Preparando contexto local...")
    return {"local_context": prepare_minimal_context(state.get("user_story", ""))}


def analyze_story(state: AgentState) -> AgentState:
    """Nó responsável por resumir a história e mapear lacunas iniciais."""
    _report_progress(state, "Analisando história e lacunas...")
    user_story = " ".join(state.get("user_story", "").strip().split())
    ambiguous_terms = detect_ambiguous_terms(user_story)

    return {
        "story_analysis": {
            "summary": user_story or "História não informada.",
            "gaps": state.get("validation_errors", []),
            "ambiguous_terms": ambiguous_terms,
            "generation_prompt": PLAN_GENERATION_SYSTEM_PROMPT,
        }
    }


def generate_acceptance_criteria(state: AgentState) -> AgentState:
    """Nó responsável por gerar critérios de aceite verificáveis."""
    _report_progress(state, "Gerando critérios de aceite...")
    story = state.get("story_analysis", {}).get("summary", state.get("user_story", ""))

    return {
        "acceptance_criteria": [
            f"Dado que o ator descrito na história tem permissão para executar a ação, quando solicita o comportamento '{story}', então o sistema deve apresentar o resultado esperado de forma observável.",
            "Dado que os dados necessários estão disponíveis, quando a ação principal é executada, então o sistema deve concluir o fluxo sem expor dados de outros usuários.",
            "Dado que não existem dados para exibir ou processar, quando o usuário executa a ação, então o sistema deve apresentar uma mensagem clara e verificável.",
        ],
        "provisional_response": {
            "acceptance_criteria_prompt": ACCEPTANCE_CRITERIA_PROMPT,
            "local_template_source": state.get("local_context", {}).get("source"),
        },
    }


def generate_test_scenarios(state: AgentState) -> AgentState:
    """Nó responsável por gerar cenários principais e negativos."""
    _report_progress(state, "Gerando cenários de teste...")
    return {
        "test_scenarios": [
            {
                "type": "principal",
                "title": "Fluxo principal executado com sucesso",
                "given": "Dado que o usuário possui perfil válido e dados compatíveis com a regra de negócio",
                "when": "Quando executa a ação descrita na história",
                "then": "Então o sistema apresenta o resultado esperado com informações completas e verificáveis",
            },
            {
                "type": "alternativo",
                "title": "Ausência de dados para a consulta ou operação",
                "given": "Dado que o usuário está autorizado, mas não possui registros aplicáveis",
                "when": "Quando executa a ação descrita na história",
                "then": "Então o sistema informa que não há dados disponíveis sem gerar erro técnico",
            },
            {
                "type": "negativo",
                "title": "Acesso sem autorização suficiente",
                "given": "Dado que o usuário não está autenticado ou não possui permissão adequada",
                "when": "Quando tenta executar a ação descrita na história",
                "then": "Então o sistema bloqueia a operação e apresenta mensagem de acesso negado",
            },
        ],
        "provisional_response": {
            **state.get("provisional_response", {}),
            "scenario_generation_prompt": SCENARIO_GENERATION_PROMPT,
        },
    }


def generate_edge_cases(state: AgentState) -> AgentState:
    """Nó responsável por sugerir casos de borda."""
    _report_progress(state, "Mapeando casos de borda...")
    return {
        "edge_cases": [
            "Executar o fluxo com exatamente um registro disponível.",
            "Executar o fluxo com volume alto de registros para verificar paginação, ordenação ou tempo de resposta definido.",
            "Verificar dados no limite de datas, valores, estados ou formatos aceitos pela regra de negócio.",
            "Validar comportamento quando dependências externas estiverem indisponíveis ou retornarem erro.",
        ]
    }


def suggest_example_data(state: AgentState) -> AgentState:
    """Nó responsável por sugerir dados de exemplo."""
    _report_progress(state, "Sugerindo dados de exemplo...")
    return {
        "example_data": [
            "Usuário válido: cliente_teste@example.com com perfil autorizado.",
            "Usuário inválido: visitante_sem_permissao@example.com sem acesso ao recurso.",
            "Entidade principal: registro 12345 com status ativo e data de referência 2026-07-18.",
            "Massa negativa: registro inexistente, campo obrigatório vazio e identificador em formato inválido.",
        ]
    }


def identify_ambiguity_risks(state: AgentState) -> AgentState:
    """Nó responsável por identificar riscos de ambiguidade."""
    _report_progress(state, "Identificando riscos e ambiguidades...")
    analysis = state.get("story_analysis", {})
    risks = [f"Lacuna: {gap}" for gap in analysis.get("gaps", [])]
    risks.extend(
        f"Termo ambíguo: '{term}' precisa de métrica ou definição objetiva."
        for term in analysis.get("ambiguous_terms", [])
    )

    if not risks:
        risks.append("Confirmar regras específicas de permissão, mensagens, ordenação, filtros e limites de volume antes da automação.")

    return {"ambiguity_risks": risks}


def suggest_automation(state: AgentState) -> AgentState:
    """Nó responsável por sugerir automação de testes."""
    _report_progress(state, "Sugerindo automação de testes...")
    return {
        "automation_suggestions": [
            "Automatizar o fluxo principal como teste de aceitação ou teste end-to-end.",
            "Criar testes de API ou serviço para permissões, estados vazios e erros esperados.",
            "Adicionar testes parametrizados para dados válidos, inválidos, mínimos e próximos aos limites.",
            "Manter cenários de ambiguidade como checklist manual até que as regras sejam objetivadas.",
        ]
    }


def _format_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _format_scenarios(scenarios: list[dict[str, str]], scenario_type: str) -> str:
    filtered_scenarios = [scenario for scenario in scenarios if scenario.get("type") == scenario_type]
    if not filtered_scenarios:
        return "- Nenhum cenário identificado."

    blocks: list[str] = []
    for scenario in filtered_scenarios:
        blocks.append(
            "\n".join(
                [
                    f"### {scenario['title']}",
                    f"- Given: {scenario['given']}",
                    f"- When: {scenario['when']}",
                    f"- Then: {scenario['then']}",
                ]
            )
        )
    return "\n\n".join(blocks)


def _build_deterministic_final_answer(state: AgentState) -> str:
    story_analysis = state.get("story_analysis", {})
    scenarios = state.get("test_scenarios", [])
    local_context = state.get("local_context", {})
    gaps_and_risks = state.get("ambiguity_risks", [])

    return "\n\n".join(
        [
            "# Plano de Testes",
            "## Resumo da história\n" + story_analysis.get("summary", "História não informada."),
            "## Lacunas e ambiguidades\n" + _format_list(gaps_and_risks),
            "## Critérios de aceite verificáveis\n" + _format_list(state.get("acceptance_criteria", [])),
            "## Cenários principais em Given/When/Then\n" + _format_scenarios(scenarios, "principal"),
            "## Cenários alternativos e negativos\n"
            + _format_scenarios(scenarios, "alternativo")
            + "\n\n"
            + _format_scenarios(scenarios, "negativo"),
            "## Casos de borda\n" + _format_list(state.get("edge_cases", [])),
            "## Dados de exemplo\n" + _format_list(state.get("example_data", [])),
            "## Sugestões de automação\n" + _format_list(state.get("automation_suggestions", [])),
            "## Riscos e observações\n"
            + _format_list(
                [
                    f"Contexto local usado: {local_context.get('source', 'não disponível')}.",
                    "Revisar critérios com pessoas de produto antes de transformar todos os cenários em automação definitiva.",
                    f"Prompt interno de formatação: {FINAL_MARKDOWN_PROMPT}",
                ]
            ),
        ]
    )


def _build_invalid_input_answer(state: AgentState) -> str:
    user_story = " ".join(state.get("user_story", "").strip().split())
    validation_errors = state.get("validation_errors", [])

    return "\n\n".join(
        [
            "# Entrada precisa de correção",
            "A entrada informada ainda não tem informações suficientes para gerar um plano de testes confiável.",
            "## Entrada recebida\n" + (user_story or "Nenhuma entrada informada."),
            "## Lacunas detectadas\n" + _format_list(validation_errors),
            "## Como corrigir\n"
            + _format_list(
                [
                    "Informe o ator ou perfil envolvido, por exemplo: Como cliente autenticado.",
                    "Descreva o objetivo ou ação esperada, por exemplo: quero consultar meus pedidos recentes.",
                    "Explique o valor ou resultado esperado, por exemplo: para acompanhar a entrega.",
                ]
            ),
            "## Exemplo de reescrita\nComo cliente autenticado, quero consultar meus pedidos recentes para acompanhar a entrega.",
        ]
    )


def format_final_answer(state: AgentState) -> AgentState:
    """Nó responsável por formatar a resposta final em Markdown."""
    _report_progress(state, "Montando resposta final...")
    if state.get("validation_errors"):
        _report_progress(state, "Entrada inválida; geração com LLM ignorada.")
        return {
            "final_answer": _build_invalid_input_answer(state),
            "generation_mode": "validation_failed",
            "fallback_used": False,
            "provisional_response": {
                **state.get("provisional_response", {}),
                "status": "invalid",
                "generation_mode": "validation_failed",
                "fallback_used": False,
                "message": "Entrada inválida; corrija as lacunas antes da geração do plano.",
            },
        }

    deterministic_answer = _build_deterministic_final_answer(state)
    provisional_response = {
        **state.get("provisional_response", {}),
        "status": "invalid" if state.get("validation_errors") else "ready",
        "message": "Plano de testes estruturado gerado com sucesso.",
    }

    config = get_llm_config()
    if config is None:
        _report_progress(state, "Nenhuma configuração de LLM encontrada; usando fallback determinístico...")
        fallback_notice = (
            "**Aviso:** fallback determinístico usado porque nenhuma configuração de LLM foi encontrada no ambiente. "
            "Defina OPENAI_API_KEY para usar geração com LLM."
        )
        return {
            "final_answer": fallback_notice + "\n\n" + deterministic_answer,
            "generation_mode": "deterministic_fallback",
            "fallback_used": True,
            "provisional_response": {
                **provisional_response,
                "generation_mode": "deterministic_fallback",
                "fallback_used": True,
                "message": "Fallback determinístico usado por ausência de configuração de LLM.",
            },
        }

    try:
        _report_progress(state, "LLM configurado; enviando solicitação ao provedor...")
        _report_progress(state, "Aguardando resposta do LLM...")
        final_answer, llm_metadata = generate_plan_with_llm(state, deterministic_answer)
    except LLMError:
        raise
    _report_progress(state, "Plano concluído com LLM.")

    return {
        "final_answer": final_answer,
        **llm_metadata,
        "provisional_response": {
            **provisional_response,
            **llm_metadata,
            "message": "Plano de testes gerado com LLM.",
        },
    }


def build_graph():
    """Constrói e compila o grafo do agente."""
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("validate_input", validate_input)
    graph_builder.add_node("prepare_context", prepare_context)
    graph_builder.add_node("analyze_story", analyze_story)
    graph_builder.add_node("generate_acceptance_criteria", generate_acceptance_criteria)
    graph_builder.add_node("generate_test_scenarios", generate_test_scenarios)
    graph_builder.add_node("generate_edge_cases", generate_edge_cases)
    graph_builder.add_node("suggest_example_data", suggest_example_data)
    graph_builder.add_node("identify_ambiguity_risks", identify_ambiguity_risks)
    graph_builder.add_node("suggest_automation", suggest_automation)
    graph_builder.add_node("format_final_answer", format_final_answer)

    graph_builder.add_edge(START, "validate_input")
    graph_builder.add_conditional_edges(
        "validate_input",
        route_after_validation,
        {
            "prepare_context": "prepare_context",
            "format_final_answer": "format_final_answer",
        },
    )
    graph_builder.add_edge("prepare_context", "analyze_story")
    graph_builder.add_edge("analyze_story", "generate_acceptance_criteria")
    graph_builder.add_edge("generate_acceptance_criteria", "generate_test_scenarios")
    graph_builder.add_edge("generate_test_scenarios", "generate_edge_cases")
    graph_builder.add_edge("generate_edge_cases", "suggest_example_data")
    graph_builder.add_edge("suggest_example_data", "identify_ambiguity_risks")
    graph_builder.add_edge("identify_ambiguity_risks", "suggest_automation")
    graph_builder.add_edge("suggest_automation", "format_final_answer")
    graph_builder.add_edge("format_final_answer", END)

    return graph_builder.compile()


def run_agent(user_story: str, progress_callback=None) -> AgentState:
    """Executa o grafo a partir de uma história de usuário."""
    graph = build_graph()
    initial_state = create_initial_state(user_story)
    if progress_callback is not None:
        initial_state["_progress_callback"] = progress_callback

    final_state = graph.invoke(initial_state)
    final_state.pop("_progress_callback", None)
    return final_state