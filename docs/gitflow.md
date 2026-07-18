# GitFlow do Projeto

Este projeto usa uma organização inspirada em GitFlow para separar desenvolvimento, entrega e manutenção.

## Branches principais

- `main`: branch de produção ou entrega estável.
- `develop`: branch de integração das próximas mudanças.

## Prefixos de branches

- `feature/`: novas funcionalidades.
- `release/`: preparação de versão ou entrega.
- `hotfix/`: correções urgentes baseadas em `main`.
- `support/`: manutenção de versões ou suporte específico.
- `chore/`: tarefas de manutenção, configuração ou organização do projeto.
- `docs/`: alterações focadas em documentação.

## Regras de uso

- Novos branches devem partir de `develop`, salvo quando a tarefa especificar outro branch de origem.
- Use nomes semânticos, por exemplo: `feature/test-plan-graph`, `docs/update-readme` ou `chore/setup-gitflow`.
- Commits devem seguir Conventional Commits: https://www.conventionalcommits.org/en/v1.0.0/#specification.
- Push só deve ser feito quando houver instrução explícita para isso.
- Pull requests devem ter como base `develop`, exceto hotfixes ou casos explicitamente definidos de outra forma.

## Configuração local aplicada

A configuração local do repositório foi inicializada com:

```text
gitflow.branch.master = main
gitflow.branch.develop = develop
gitflow.prefix.feature = feature/
gitflow.prefix.release = release/
gitflow.prefix.hotfix = hotfix/
gitflow.prefix.support = support/
gitflow.prefix.versiontag =
```

Essa configuração fica em `.git/config` e não é versionada pelo Git. Por isso, este documento registra o padrão esperado para novas sessões e outros ambientes.
