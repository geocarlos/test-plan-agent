"""Prompts internos para geração do plano de testes."""

PLAN_GENERATION_SYSTEM_PROMPT = """
Você é um agente de planejamento de testes. Gere uma resposta objetiva, verificável
e adequada a uma entrega acadêmica prática, usando a história informada e a base
local de templates como referência.
""".strip()

ACCEPTANCE_CRITERIA_PROMPT = """
Transforme a história em critérios de aceite observáveis, preferindo formato
Dado/Quando/Então e evitando termos subjetivos sem métrica.
""".strip()

SCENARIO_GENERATION_PROMPT = """
Crie cenários principais, alternativos e negativos em Given/When/Then, cobrindo
sucesso, acesso indevido, estado vazio e falhas esperadas.
""".strip()

FINAL_MARKDOWN_PROMPT = """
Formate o plano final em Markdown com resumo, lacunas, critérios, cenários,
casos de borda, dados de exemplo, automação, riscos e observações.
""".strip()

LLM_TEST_PLAN_PROMPT = """
Gere o plano de testes final em Markdown para a história abaixo.

Regras obrigatórias:
- Escreva em português do Brasil.
- Use a base local de templates como contexto de apoio.
- Preserve uma estrutura verificável com as seções: Resumo da história, Lacunas e ambiguidades, Critérios de aceite verificáveis, Cenários principais em Given/When/Then, Cenários alternativos e negativos, Casos de borda, Dados de exemplo, Sugestões de automação, Riscos e observações.
- Não invente credenciais, dados sensíveis, chaves, tokens ou informações pessoais reais.
- Quando houver lacunas, deixe claro o que precisa ser confirmado com produto ou negócio.

História original:
{user_story}

Resumo normalizado:
{story_summary}

Lacunas detectadas antes da geração:
{validation_errors}

Contexto local usado ({local_context_source}):
{local_context}

Rascunho determinístico de apoio:
{deterministic_draft}
""".strip()
