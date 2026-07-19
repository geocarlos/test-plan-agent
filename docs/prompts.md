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

## Prompt 4: Geração do plano de testes

### Objetivo

Implementar a geração estruturada do plano de testes, com prompts internos, novos nós no grafo, enriquecimento do estado de execução e formatação da resposta final em Markdown.

### Branch sugerido

```text
feature/test-plan-generation
```

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Contexto já concluído:
- O setup inicial Python com uv já foi realizado.
- O esqueleto do agente LangGraph já existe com state.py, graph.py, tools.py, validators.py e cli.py.
- A base local `data/test_templates.md` já existe.
- A ferramenta de leitura controlada da base local já foi implementada com validações de segurança.
- O grafo já usa a base local como contexto.
- O CLI executa com `uv run test-plan-agent`.
- A suíte atual passa com `uv run pytest`.

Objetivo do projeto:
Construir um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis com critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.

Nesta etapa, implemente a geração do plano de testes final, ainda sem depender obrigatoriamente de chamada real a LLM. Se não houver configuração explícita de provedor de IA no projeto, use uma geração determinística e estruturada baseada na história do usuário e na base local de templates.

Branch sugerido para esta etapa:
feature/test-plan-generation

Regras do projeto:
- Faça somente o que for pedido nesta etapa.
- Use documentação em português com acentuação correta conforme a ortografia padrão do Brasil.
- Preserve as instruções do projeto em .github/copilot-instructions.md, .github/instructions/project-memory.instructions.md e CLAUDE.md.
- Não adicione banco de dados ou memória persistente nesta etapa.
- Use o estado do LangGraph como memória de execução.
- Não adicione chamadas reais a LLM sem configuração explícita e segura.
- Mantenha a saída final verificável, objetiva e adequada a uma entrega acadêmica prática.

Tarefas esperadas:
1. Atualizar `src/test_plan_agent/state.py` para representar melhor a memória de execução, incluindo campos como `acceptance_criteria`, `test_scenarios`, `edge_cases`, `example_data`, `ambiguity_risks`, `automation_suggestions` e `final_answer`.
2. Criar ou atualizar um módulo de prompts internos, por exemplo `src/test_plan_agent/prompts.py`, com templates textuais usados pela geração do plano.
3. Melhorar `src/test_plan_agent/validators.py` para sinalizar lacunas básicas da história, como ausência de ator, objetivo ou resultado esperado.
4. Adicionar detecção simples de termos ambíguos, como "rápido", "simples", "intuitivo", "adequado", "melhor" e "completo".
5. Atualizar `src/test_plan_agent/graph.py` com nós claros para analisar a história, gerar critérios de aceite, gerar cenários, gerar casos de borda, sugerir dados de exemplo, identificar riscos de ambiguidade e formatar a resposta final.
6. Garantir que o grafo continue usando `data/test_templates.md` como contexto por meio da ferramenta controlada.
7. Gerar uma resposta final em Markdown com seções como:
	- Resumo da história
	- Lacunas e ambiguidades
	- Critérios de aceite verificáveis
	- Cenários principais em Given/When/Then
	- Cenários alternativos e negativos
	- Casos de borda
	- Dados de exemplo
	- Sugestões de automação
	- Riscos e observações
8. Atualizar `src/test_plan_agent/cli.py` para imprimir a resposta final em Markdown quando o fluxo for executado.
9. Atualizar ou criar testes em `tests/` cobrindo história válida, história curta ou inválida, termos ambíguos, geração das principais seções e uso do contexto local.
10. Atualizar o README.md somente se houver mudança real no comportamento demonstrável do CLI.
11. Validar tudo com comandos reais usando uv.

Resultado esperado:
- Estado do agente enriquecido como memória de execução.
- Prompts internos registrados no código.
- Grafo com nós de geração do plano de testes.
- Resposta final formatada em Markdown.
- Validações básicas mais fortes para entrada e ambiguidade.
- `uv run test-plan-agent` exibindo um plano de testes estruturado.
- `uv run pytest` passando.

Ao final, informe os arquivos alterados, os comandos executados, o resultado dos testes e o que ficou preparado para a próxima etapa.
```

### Resultado esperado

- Plano de testes final gerado em Markdown.
- Estado do LangGraph usado como memória de execução enriquecida.
- Nós do grafo separados para análise, geração e formatação.
- Validação de entrada e ambiguidade mais robusta.
- CLI demonstrando a saída final estruturada.
- Testes cobrindo a geração principal e casos inválidos.

### Status

- Concluído e validado com `uv run test-plan-agent`, `uv run python -m test_plan_agent.cli "Como cliente, quero uma busca rápida e intuitiva para encontrar pedidos."` e `uv run pytest`.

## Prompt 5: Testes e exemplos

### Objetivo

Ampliar a cobertura de testes e criar exemplos versionados de entrada e saída para demonstrar o funcionamento do agente de forma clara, reproduzível e alinhada aos critérios de entrega do mini-projeto.

### Branch sugerido

```text
test/add-examples-and-coverage
```

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Contexto já concluído:
- O setup inicial Python com uv já foi realizado.
- O esqueleto do agente LangGraph já existe.
- A ferramenta de leitura controlada da base local já existe.
- A geração do plano de testes final em Markdown já foi implementada.
- O CLI executa com `uv run test-plan-agent`.
- A suíte atual passa com `uv run pytest`.

Objetivo do projeto:
Construir um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis com critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.

Nesta etapa, adicione testes e exemplos de entrada/saída para tornar a solução demonstrável e pronta para automação futura em CI.

Branch sugerido para esta etapa:
test/add-examples-and-coverage

Regras do projeto:
- Faça somente o que for pedido nesta etapa.
- Use documentação em português com acentuação correta conforme a ortografia padrão do Brasil.
- Preserve as instruções do projeto em .github/copilot-instructions.md, .github/instructions/project-memory.instructions.md e CLAUDE.md.
- Não altere a arquitetura principal do agente, salvo se uma falha de teste revelar ajuste pequeno e necessário.
- Não adicione GitHub Actions nesta etapa; isso fica para a próxima etapa.
- Mantenha exemplos sem dados sensíveis, tokens, chaves ou informações pessoais reais.

Tarefas esperadas:
1. Revisar a suíte atual em `tests/` e separar ou complementar testes quando isso melhorar a organização.
2. Adicionar testes para execução completa do agente com história válida.
3. Adicionar testes para histórias inválidas ou incompletas, incluindo ausência de ator, objetivo ou resultado esperado.
4. Adicionar testes para termos ambíguos e para a presença das principais seções da resposta final.
5. Adicionar testes para garantir que o contexto local de `data/test_templates.md` continua sendo usado.
6. Criar exemplos versionados de entrada, por exemplo em `examples/input/` ou `data/examples/`, com histórias de usuário válidas, ambíguas e incompletas.
7. Criar exemplos versionados de saída, por exemplo em `examples/output/`, mostrando planos de teste gerados em Markdown.
8. Atualizar o README.md com uma seção de exemplos de execução, apontando para os arquivos criados e mantendo comandos com `uv`.
9. Garantir que `uv run pytest` seja o comando principal de validação da suíte.
10. Executar comandos reais de validação com uv.

Resultado esperado:
- Testes mais organizados e cobrindo os principais comportamentos do agente.
- Exemplos de entrada versionados.
- Exemplos de saída em Markdown versionados.
- README.md apontando para os exemplos e comandos de execução.
- `uv run test-plan-agent` funcionando.
- `uv run pytest` passando.

Ao final, informe os arquivos alterados, os comandos executados, o resultado dos testes e o que ficou preparado para a próxima etapa de CI/GitHub Actions.
```

### Resultado esperado

- Suíte de testes ampliada e mais representativa.
- Exemplos de entrada e saída versionados no repositório.
- README atualizado com exemplos de uso.
- Comando `uv run pytest` validando o comportamento principal do agente.
- Projeto preparado para criação de workflow de CI na próxima etapa.

### Status

- Concluído e validado com `uv run pytest` e `uv run test-plan-agent`.

## Prompt 6: CI/GitHub Actions

### Objetivo

Criar um workflow de GitHub Actions para validar automaticamente o projeto com `uv`, executando instalação de dependências, testes e uma execução básica do CLI em pull requests e pushes relevantes.

### Branch sugerido

```text
ci/add-github-actions-workflow
```

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Contexto já concluído:
- O projeto Python usa uv.
- O agente com LangGraph já gera planos de teste em Markdown.
- A ferramenta de leitura controlada da base local já existe.
- A suíte de testes foi ampliada.
- Existem exemplos versionados de entrada e saída.
- O comando `uv run pytest` passa localmente.
- O comando `uv run test-plan-agent` executa localmente.

Objetivo do projeto:
Construir um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis com critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.

Nesta etapa, crie apenas a configuração de CI com GitHub Actions.

Branch sugerido para esta etapa:
ci/add-github-actions-workflow

Regras do projeto:
- Faça somente o que for pedido nesta etapa.
- Use documentação em português com acentuação correta conforme a ortografia padrão do Brasil.
- Preserve as instruções do projeto em .github/copilot-instructions.md, .github/instructions/project-memory.instructions.md e CLAUDE.md.
- Não altere a lógica do agente, salvo se a configuração de CI revelar um problema mínimo e necessário.
- Não adicione serviços externos, banco de dados, secrets ou tokens.
- Não exponha credenciais ou valores sensíveis.

Tarefas esperadas:
1. Criar `.github/workflows/ci.yml`.
2. Configurar o workflow para rodar em pull requests para `develop` e `main`.
3. Configurar o workflow para rodar em pushes para `develop` e `main`.
4. Usar uma versão fixa ou controlada de Python compatível com `pyproject.toml`.
5. Instalar ou configurar `uv` no workflow usando uma action adequada e conhecida.
6. Executar `uv sync`.
7. Executar `uv run pytest`.
8. Executar uma validação simples do CLI, por exemplo `uv run test-plan-agent`.
9. Se fizer sentido, executar o CLI com uma história curta de exemplo para garantir que a saída final em Markdown é gerada sem erro.
10. Atualizar o README.md apenas se for útil documentar o status ou comando de CI.
11. Validar localmente a sintaxe YAML sempre que possível e explicar qualquer limitação de validação local.

Resultado esperado:
- Workflow `.github/workflows/ci.yml` criado.
- CI validando instalação, testes e execução básica do agente.
- Nenhuma dependência desnecessária adicionada.
- Nenhum secret ou token exigido.
- Projeto pronto para usar checks automáticos em PRs.

Ao final, informe os arquivos alterados, os comandos executados, as validações feitas e qualquer limitação encontrada por não ser possível executar GitHub Actions localmente.
```

### Resultado esperado

- Workflow de CI criado em `.github/workflows/ci.yml`.
- CI executando `uv sync`, `uv run pytest` e validação básica do CLI.
- Workflow acionado em pull requests e pushes para `develop` e `main`.
- Projeto preparado para checks automáticos no GitHub.

### Status

- Concluído e validado com `uv sync --locked`, `uv run pytest`, `uv run test-plan-agent` e execução do CLI com uma história curta gerando Markdown.

## Prompt 7: Entrada por Markdown e visualização da documentação

### Objetivo

Melhorar a experiência de uso e apresentação do agente adicionando entrada por arquivo Markdown no CLI e diagramas Mermaid coloridos na documentação principal.

### Branch sugerido

```text
docs/final-delivery-review
```

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Contexto já concluído:
- O agente com LangGraph já gera planos de teste em Markdown.
- O CLI já aceita uma história de usuário como argumento de linha de comando.
- O projeto possui README, exemplos versionados, testes automatizados e CI.

Objetivo desta melhoria:
Adicionar suporte para informar a história de usuário por caminho de arquivo Markdown e melhorar a documentação com visualizações Mermaid coloridas.

Tarefas esperadas:
1. Atualizar o CLI para aceitar uma opção como `--file` ou `-f` apontando para um arquivo Markdown.
2. Ler o conteúdo do arquivo Markdown como entrada do agente.
3. Evitar uso simultâneo de argumento textual e arquivo.
4. Retornar erros controlados para extensão inválida ou arquivo inexistente.
5. Adicionar testes cobrindo entrada padrão, leitura de Markdown, extensão inválida e conflito entre argumento e arquivo.
6. Criar um exemplo versionado de entrada Markdown.
7. Atualizar o README.md com o novo modo de execução.
8. Adicionar ao README.md uma visualização geral e um fluxo do agente usando Mermaid com cores por tipo de etapa.
9. Validar tudo com comandos reais usando uv.

Resultado esperado:
- CLI aceitando entrada por arquivo Markdown.
- README com diagramas Mermaid coloridos e visão geral do agente.
- Exemplo Markdown versionado.
- Testes passando.
```

### Resultado esperado

- Nova opção `--file` no CLI para ler histórias a partir de arquivos `.md` ou `.markdown`.
- Exemplo versionado em `examples/input/historia-valida.md`.
- README com comandos de execução por arquivo e diagramas Mermaid coloridos.
- Testes cobrindo a resolução de entrada por argumento, arquivo e casos inválidos.

### Status

- Concluído e validado com `uv run pytest`, `uv run test-plan-agent --file .\examples\input\historia-valida.md` e `git diff --check`.

## Fix Prompt: Arquivo Markdown com múltiplas user stories

### Objetivo

Corrigir o comportamento do CLI ao receber um arquivo Markdown contendo várias user stories, garantindo que cada história seja processada separadamente pelo agente e que o resultado final seja gerado com um plano de testes por história.

### Branch sugerido

```text
fix/multiple-user-stories-file
```

### Prompt

```text
Estamos no repositório test-plan-agent, um mini-projeto avaliativo do curso IA para Desenvolvedores.

Contexto já concluído:
- O agente com LangGraph já gera planos de teste em Markdown.
- O CLI já aceita entrada textual e entrada por arquivo Markdown usando `--file`.
- A documentação, exemplos, testes e CI já existem.
- O terminal deve estar dentro de `./test-plan-agent`.
- O branch base é `develop`, a partir do qual o branch de correção deve ser criado.

Problema observado:
O comando abaixo não gera o resultado esperado quando o arquivo informado contém várias histórias de usuário:

`uv run .\test-plan-agent\src\test_plan_agent\cli.py --file .\user_stories_airtable_crm.md > output.md`

O arquivo Markdown possui múltiplas user stories separadas por blocos, mas o CLI concatena todo o conteúdo em uma única entrada. Com isso, o grafo executa uma vez só e produz um plano de testes genérico para todas as histórias misturadas.

Objetivo do fix:
1. Criar um branch de correção a partir de `develop`, usando nome semântico iniciado por `fix/`.
2. Analisar como o agente está implementado, principalmente o caminho de entrada por arquivo no CLI.
3. Ajustar a leitura de arquivos Markdown para aceitar uma ou mais user stories.
4. Quando o arquivo tiver várias histórias separadas por `---`, executar o agente uma vez por história.
5. Manter compatibilidade com arquivos Markdown contendo uma única história.
6. Garantir que o comando direto com `uv run caminho\cli.py` funcione a partir da raiz do workspace.
7. Corrigir problemas de acentuação na saída redirecionada para `output.md` no Windows.
8. Criar testes para arquivos com múltiplas user stories.
9. Adicionar teste de ponta a ponta do CLI garantindo que múltiplas histórias gerem múltiplos planos.
10. Atualizar o README.md para documentar o suporte a várias histórias em um mesmo arquivo Markdown.
11. Registrar este fix em `docs/prompts.md` como uma seção independente, sem usar a numeração sequencial dos prompts anteriores.
12. Validar tudo com comandos reais usando `uv`.

Resultado esperado:
- Branch `fix/multiple-user-stories-file` criado a partir de `develop`.
- CLI lendo arquivos Markdown com uma ou várias histórias.
- Arquivos com múltiplas histórias separados por `---` gerando um plano de testes para cada história.
- Saída redirecionada para `output.md` com acentuação correta.
- Comando direto com `uv run .\test-plan-agent\src\test_plan_agent\cli.py --file .\user_stories_airtable_crm.md > output.md` funcionando.
- Testes automatizados cobrindo parser de múltiplas histórias e comportamento final do CLI.
- README.md atualizado com o novo comportamento.
- `uv run pytest` passando.

Ao final, informe os arquivos alterados, comandos executados, resultado dos testes e o status do branch, sem realizar commit automaticamente.
```

### Resultado esperado

- Correção documentada em branch próprio de fix.
- Leitura de Markdown com múltiplas user stories suportada no CLI.
- Execução do agente feita individualmente para cada história encontrada.
- Testes cobrindo parser e execução final do CLI com múltiplas histórias.
- README atualizado com o formato esperado para arquivos Markdown com vários blocos.

### Status

- Concluído e validado com `uv run pytest` e execução do comando original com redirecionamento para `output.md`.
