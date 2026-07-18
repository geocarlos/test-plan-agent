---
description: "Use when working anywhere in the Test-Plan Agent project. Stores evolving project-wide memory, recurring rules, scope limits, documentation language rules, and agent behavior preferences."
name: "Test-Plan Agent Project Memory"
applyTo: "**"
---

# Memória do Projeto

Este arquivo funciona como uma memória evolutiva do projeto para o GitHub Copilot. Adicione aqui novas regras quando elas precisarem valer ao longo de todo o repositório e em sessões futuras.

## Contexto geral

- Projeto: **Test-Plan Agent**.
- Objetivo: criar um agente com LangGraph que receba histórias de usuário, issues ou requisitos funcionais e gere planos de teste verificáveis.
- Saída esperada: critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda, dados de exemplo, riscos de ambiguidade e sugestões de automação.
- Guia principal: `docs/guia-geral-prompt.md`.

## Regras permanentes

- Faça somente o que foi pedido explicitamente.
- Não avance para etapas adicionais sem confirmação do usuário.
- Se o pedido for "stage and commit the current changes", limite-se a stage e commit. Não faça push, não crie PR e não faça merge sem uma nova instrução explícita.
- Preserve mudanças existentes do usuário e não reverta alterações não relacionadas ao pedido atual.
- Documentos em português, inclusive prompts, devem usar acentuação conforme a ortografia padrão do Brasil.
- Evite remover acentos de textos em português, salvo limitação técnica explícita.
- Use nomes semânticos para branches, indicando tipo e objetivo da mudança.
- Use Conventional Commits em mensagens de commit: https://www.conventionalcommits.org/en/v1.0.0/#specification.
- Ao receber instrução para criar um novo branch, assuma sempre a criação a partir de `develop`, a menos que a instrução especifique outro branch de origem.
- Sugira criar um novo branch ao receber instruções que pareçam relacionadas a outra etapa e não façam sentido no branch atual. Obtenha confirmação antes de criar o branch.
- Sugira commit ao completar tarefas que pareçam fechar um ciclo, etapa ou sub-etapa.
- Faça push somente quando receber instrução explícita para isso.

## Como atualizar esta memória

- Adicione regras novas como bullets curtos e acionáveis.
- Evite duplicar conteúdo detalhado do README ou de documentos técnicos.
- Prefira registrar decisões recorrentes, restrições de escopo e preferências que realmente impactem o trabalho futuro.
