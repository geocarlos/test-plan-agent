# Instruções do Projeto para Agentes

Este arquivo registra orientações para agentes que trabalham neste repositório, especialmente quando a ferramenta lê `CLAUDE.md` como contexto de projeto.

Para GitHub Copilot, o equivalente nativo está em `.github/copilot-instructions.md`. Mantenha ambos alinhados quando uma regra precisar valer para qualquer assistente usado no projeto.

## Contexto geral

- Projeto: **Test-Plan Agent**.
- Objetivo: criar um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis.
- Saída esperada do agente: critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.
- Documento de planejamento principal: `docs/guia-geral-prompt.md`.

## Regras de atuação

- Faça somente o que foi pedido explicitamente.
- Não encadeie ações adicionais sem confirmação. Por exemplo, se o pedido for "stage and commit the current changes", não faça push, não crie PR e não faça merge por iniciativa própria.
- Quando uma próxima ação parecer útil, ofereça a opção ao usuário, mas aguarde confirmação antes de executá-la.
- Preserve mudanças existentes feitas pelo usuário. Não reverta arquivos ou trechos não relacionados à tarefa atual.
- Prefira mudanças pequenas, rastreáveis e alinhadas ao escopo do mini-projeto.

## Git e versionamento

- Use nomes semânticos para branches, indicando tipo e objetivo da mudança.
- Use Conventional Commits em mensagens de commit: https://www.conventionalcommits.org/en/v1.0.0/#specification.
- Ao receber instrução para criar um novo branch, assuma sempre a criação a partir de `develop`, a menos que a instrução especifique outro branch de origem.
- Sugira criar um novo branch ao receber instruções que pareçam relacionadas a outra etapa e não façam sentido no branch atual. Obtenha confirmação antes de criar o branch.
- Sugira commit ao completar tarefas que pareçam fechar um ciclo, etapa ou sub-etapa.
- Faça push somente quando receber instrução explícita para isso.

## Idioma e documentação

- Documentos do projeto em português devem usar acentuação conforme a ortografia padrão do Brasil.
- Prompts escritos em português também devem usar acentuação correta.
- Evite remover acentos de textos em português, salvo quando houver limitação técnica explícita.
- Mantenha linguagem clara, objetiva e adequada a uma entrega acadêmica prática.

## Memória evolutiva do projeto

- Novas regras globais do projeto devem ser adicionadas também em `.github/instructions/project-memory.instructions.md`.
- Use essa memória para registrar decisões recorrentes, restrições e preferências que devem continuar valendo em novas sessões.
