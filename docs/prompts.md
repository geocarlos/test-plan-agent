# Prompts Utilizados

Este arquivo registra os principais prompts usados para planejar, implementar, corrigir e melhorar o **Test-Plan Agent**, conforme exigido pelo mini-projeto avaliativo do Módulo 2.

A cada etapa, registre aqui o prompt planejado, execute-o em uma sessão dedicada do GitHub Copilot e, ao finalizar a etapa, retorne para registrar o próximo prompt.

## Prompt 1: Setup inicial Python com uv

### Objetivo

Criar a base técnica do projeto Python usando `uv`, preparando estrutura de arquivos, dependências, scripts e comandos iniciais de execução.

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Objetivo do projeto:
Construir um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis com critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.

Nesta etapa, faça apenas o setup inicial do projeto Python usando uv.

Regras do projeto:
- Faça somente o que for pedido nesta etapa.
- Use documentação em português com acentuação correta conforme a ortografia padrão do Brasil.
- Preserve as instruções do projeto em .github/copilot-instructions.md, .github/instructions/project-memory.instructions.md e CLAUDE.md.
- Use nomes e estrutura claros, adequados para uma entrega acadêmica prática.
- Não implemente ainda o agente LangGraph completo. Crie apenas a base para as próximas etapas.

Tarefas esperadas:
1. Configurar o projeto com uv.
2. Criar ou atualizar pyproject.toml com metadados básicos do projeto.
3. Adicionar dependências necessárias para a futura implementação com LangGraph e uso de variáveis de ambiente, sem adicionar dependências desnecessárias.
4. Criar uma estrutura inicial de código em src/ adequada ao projeto.
5. Criar uma estrutura inicial de testes em tests/.
6. Criar ou atualizar .gitignore para ignorar arquivos sensíveis, ambientes virtuais, caches e saídas geradas.
7. Criar .env.example apenas com nomes de variáveis, sem valores reais.
8. Atualizar o README.md com instruções iniciais de instalação e execução usando uv.
9. Validar o setup com comandos reais do uv sempre que possível.

Resultado esperado:
- pyproject.toml configurado.
- Estrutura inicial do projeto criada.
- .gitignore e .env.example criados ou atualizados.
- README.md com instruções usando uv.
- Pelo menos um comando de validação executado com sucesso.

Ao final, informe os arquivos alterados, os comandos executados e qualquer limitação encontrada.
```

### Resultado esperado

- Projeto Python inicializado com `uv`.
- Estrutura mínima criada para código e testes.
- Dependências iniciais registradas.
- README atualizado com comandos de setup e execução.
- Arquivos de segurança básicos criados, como `.gitignore` e `.env.example`.

### Status

- Concluído e validado com `uv run test-plan-agent` e `uv run pytest`.

## Prompt 2: Esqueleto do agente LangGraph

### Objetivo

Criar o esqueleto funcional do agente com LangGraph, organizando estado, grafo, validações, ferramenta mínima e ponto de entrada, sem implementar ainda a geração completa do plano de testes.

### Branch sugerido

```text
feature/langgraph-agent-skeleton
```

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Contexto já concluído:
- O setup inicial Python com uv já foi realizado.
- O projeto possui pyproject.toml, src/, tests/, .gitignore, .env.example e comandos básicos com uv.
- O CLI inicial executa com `uv run test-plan-agent`.
- A suíte inicial executa com `uv run pytest`.

Objetivo do projeto:
Construir um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis com critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.

Nesta etapa, faça apenas o esqueleto funcional do agente LangGraph.

Branch sugerido para esta etapa:
feature/langgraph-agent-skeleton

Regras do projeto:
- Faça somente o que for pedido nesta etapa.
- Use documentação em português com acentuação correta conforme a ortografia padrão do Brasil.
- Preserve as instruções do projeto em .github/copilot-instructions.md, .github/instructions/project-memory.instructions.md e CLAUDE.md.
- Use nomes claros e semânticos para módulos, funções, estado e nós do grafo.
- Não implemente ainda a geração completa do plano de testes. Crie um fluxo mínimo, testável e preparado para evolução.
- Não adicione chamadas reais a LLM nesta etapa, a menos que já exista configuração explícita para isso no projeto.

Tarefas esperadas:
1. Criar ou atualizar `src/test_plan_agent/state.py` com o estado compartilhado do agente.
2. Criar ou atualizar `src/test_plan_agent/validators.py` com validação básica da história de usuário.
3. Criar ou atualizar `src/test_plan_agent/tools.py` com uma ferramenta mínima controlada, mesmo que temporária, para preparar o uso futuro de contexto local.
4. Criar ou atualizar `src/test_plan_agent/graph.py` com um `StateGraph` mínimo funcionando.
5. Atualizar `src/test_plan_agent/cli.py` para executar o fluxo mínimo do grafo com uma entrada de exemplo ou argumento simples.
6. Criar ou atualizar testes em `tests/` cobrindo o estado, a validação e a execução mínima do grafo.
7. Atualizar o README.md somente se houver mudança real nos comandos de execução.
8. Validar tudo com comandos reais usando uv.

Fluxo mínimo esperado:
Entrada da história de usuário
→ validação da entrada
→ preparação de contexto mínimo
→ geração de uma resposta provisória estruturada
→ retorno do estado final

Resultado esperado:
- `state.py`, `graph.py`, `tools.py`, `validators.py` e `cli.py` criados ou atualizados.
- Fluxo mínimo com LangGraph executando sem erro.
- Testes cobrindo o fluxo básico.
- `uv run test-plan-agent` funcionando.
- `uv run pytest` passando.

Ao final, informe os arquivos alterados, os comandos executados, o resultado dos testes e o que ficou preparado para a próxima etapa.
```

### Resultado esperado

- Esqueleto do agente com `StateGraph` funcional.
- Estado compartilhado definido.
- Validação básica de entrada implementada.
- Ferramenta mínima criada para evolução posterior.
- CLI executando o fluxo básico.
- Testes passando com `uv run pytest`.

### Status

- Concluído e validado com `uv run test-plan-agent` e `uv run pytest`.

## Prompt 3: Base local e ferramenta

### Objetivo

Criar a base local de templates e exemplos de testes, implementar uma ferramenta de leitura controlada e adicionar validações de segurança para acesso a arquivos locais.

### Branch sugerido

```text
feature/local-test-template-tool
```

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Contexto já concluído:
- O setup inicial Python com uv já foi realizado.
- O esqueleto do agente LangGraph já existe com state.py, graph.py, tools.py, validators.py e cli.py.
- O CLI executa o fluxo mínimo com `uv run test-plan-agent`.
- A suíte atual passa com `uv run pytest`.

Objetivo do projeto:
Construir um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis com critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.

Nesta etapa, implemente apenas a base local de templates e a ferramenta controlada de leitura dessa base.

Branch sugerido para esta etapa:
feature/local-test-template-tool

Regras do projeto:
- Faça somente o que for pedido nesta etapa.
- Use documentação em português com acentuação correta conforme a ortografia padrão do Brasil.
- Preserve as instruções do projeto em .github/copilot-instructions.md, .github/instructions/project-memory.instructions.md e CLAUDE.md.
- Não implemente ainda a geração completa do plano de testes.
- Não adicione chamadas reais a LLM nesta etapa.
- Priorize segurança no acesso a arquivos locais.

Tarefas esperadas:
1. Criar `data/test_templates.md` com templates e exemplos úteis para critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda e checklist de testabilidade.
2. Atualizar `src/test_plan_agent/tools.py` com uma ferramenta real de leitura controlada da base local.
3. Garantir que a ferramenta permita leitura apenas dentro da pasta `data/`.
4. Permitir apenas arquivos `.md` e `.txt` na ferramenta de leitura.
5. Limitar o tamanho máximo do arquivo lido para evitar processamento excessivo.
6. Retornar erros controlados para arquivo inexistente, extensão inválida, tentativa de path traversal ou arquivo grande demais.
7. Integrar a ferramenta ao fluxo mínimo do grafo em `src/test_plan_agent/graph.py`, substituindo ou expandindo o contexto mínimo atual.
8. Atualizar ou criar testes em `tests/` para cobrir leitura válida, arquivo inexistente, extensão inválida e tentativa de leitura fora da pasta permitida.
9. Atualizar o README.md somente se houver mudança real nos comandos ou comportamento demonstrável.
10. Validar tudo com comandos reais usando uv.

Resultado esperado:
- `data/test_templates.md` criado.
- Ferramenta de leitura controlada implementada.
- O grafo usa a base local como contexto.
- Validações de segurança da ferramenta cobertas por testes.
- `uv run test-plan-agent` funcionando.
- `uv run pytest` passando.

Ao final, informe os arquivos alterados, os comandos executados, o resultado dos testes e o que ficou preparado para a próxima etapa.
```

### Resultado esperado

- Base local de templates criada em `data/test_templates.md`.
- Ferramenta real de leitura controlada implementada em `tools.py`.
- Validações de segurança para leitura local implementadas.
- Grafo usando a base local como contexto para a resposta provisória.
- Testes cobrindo cenários positivos e negativos da ferramenta.

### Status

- Concluído e validado com `uv run test-plan-agent` e `uv run pytest`.
