# Project Guidelines

## Contexto geral

- Este repositório contém o **Test-Plan Agent**, mini-projeto do curso IA para Desenvolvedores.
- O objetivo é construir um agente com LangGraph que transforme histórias de usuário, issues ou requisitos funcionais em planos de teste verificáveis.
- A saída principal deve incluir critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.
- Consulte `docs/guia-geral-prompt.md` antes de alterar decisões centrais de produto, fluxo ou formato de resposta.

## Escopo de atuação

- Faça somente o que foi pedido explicitamente pelo usuário.
- Não execute próximas etapas por iniciativa própria sem confirmação. Se o usuário pedir para stage e commit, não faça push, não crie PR e não faça merge.
- Você pode sugerir uma próxima tarefa útil, mas deve aguardar confirmação antes de executá-la.
- Preserve alterações existentes do usuário e não reverta mudanças não relacionadas ao pedido atual.

## Git e versionamento

- Use nomes semânticos para branches, indicando tipo e objetivo da mudança.
- Use Conventional Commits em mensagens de commit: https://www.conventionalcommits.org/en/v1.0.0/#specification.
- Ao receber instrução para criar um novo branch, assuma sempre a criação a partir de `develop`, a menos que a instrução especifique outro branch de origem.
- Sugira criar um novo branch ao receber instruções que pareçam relacionadas a outra etapa e não façam sentido no branch atual. Obtenha confirmação antes de criar o branch.
- Sugira commit ao completar tarefas que pareçam fechar um ciclo, etapa ou sub-etapa.
- Faça push somente quando receber instrução explícita para isso.

## Documentação e idioma

- Documentos em português, inclusive prompts, devem conter acentuação conforme a ortografia padrão do Brasil.
- Não remova acentos de textos em português salvo limitação técnica explícita.
- Mantenha documentação clara, objetiva e adequada a uma entrega acadêmica prática.

## Memória do projeto

- Regras globais novas devem ser registradas em `.github/instructions/project-memory.instructions.md` quando precisarem continuar valendo em sessões futuras.
- Mantenha essa memória curta, acionável e focada em decisões realmente recorrentes.
