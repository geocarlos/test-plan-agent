# Test-Plan Agent

Agente de IA para planejar testes manuais e automatizados a partir de histórias de usuário.

Este repositório será desenvolvido como mini-projeto do curso **IA para Desenvolvedores** do **SCTEC**.

## Objetivo inicial

Construir um agente com LangGraph capaz de receber uma história de usuário, analisar o contexto e gerar um plano de testes estruturado com critérios de aceite, cenários principais, casos de borda e sugestões de automação.

## Planejamento

O guia inicial do agente está em [docs/guia-geral-prompt.md](docs/guia-geral-prompt.md). Ele descreve o prompt-base, fluxo com LangGraph, estado recomendado, ferramenta integrada, validações e exemplos de entrada e saída.

## Setup inicial

Este projeto usa Python com `uv` para gerenciamento de ambiente, dependências e execução de comandos.

### Pré-requisitos

- Python 3.12 ou superior.
- `uv` instalado e disponível no terminal.

### Instalação

Na raiz do repositório, execute:

```bash
uv sync
```

Para configurar variáveis de ambiente locais, copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
```

Preencha o arquivo `.env` local apenas com valores reais da sua máquina. Esse arquivo não deve ser versionado.

### Execução

O ponto de entrada inicial pode ser executado com:

```bash
uv run test-plan-agent
```

Também é possível executar o módulo diretamente:

```bash
uv run python -m test_plan_agent.cli
```

### Testes

Execute a suíte inicial com:

```bash
uv run pytest
```

## GitFlow

O fluxo de branches do projeto está documentado em [docs/gitflow.md](docs/gitflow.md).

## Status

Projeto em fase inicial, com base Python configurada para as próximas etapas de implementação com LangGraph.