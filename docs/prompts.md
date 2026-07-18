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

- Planejado.
