"""Prompts internos para geração determinística do plano de testes."""

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
