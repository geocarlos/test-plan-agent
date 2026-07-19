# Apresentação do Test-Plan Agent

## Slide 1: Problema e proposta

**Problema:** histórias de usuário podem chegar ao time com lacunas, termos ambíguos e critérios de aceite pouco verificáveis, dificultando o planejamento de testes.

**Proposta:** criar um agente com LangGraph que recebe uma história de usuário e gera um plano de testes estruturado em Markdown.

**Entrada:** história de usuário, issue ou requisito funcional em texto.

**Saída:** critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.

---

## Slide 2: Fluxo e implementação

**Fluxo do agente:** validação da entrada -> leitura controlada da base local -> análise da história -> geração de critérios e cenários -> identificação de riscos -> formatação final em Markdown.

**Tecnologias:** Python, uv, LangGraph, pytest e GitHub Actions.

**Ferramenta integrada:** leitura controlada de `data/test_templates.md`, restrita à pasta `data/`, com extensões permitidas e limite de tamanho.

**Cuidados de entrega:** sem chaves ou tokens versionados, exemplos de entrada e saída no repositório, prompts registrados em `docs/prompts.md`, testes automatizados e CI em pull requests e pushes para `develop` e `main`.