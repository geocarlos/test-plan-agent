# Test-Plan Agent

Agente de IA para planejar testes manuais e automatizados a partir de histórias de usuário.

Este repositório será desenvolvido como mini-projeto do curso **IA para Desenvolvedores** do **SCTEC**.

## Objetivo inicial

Construir um agente com LangGraph capaz de receber uma história de usuário, analisar o contexto e gerar um plano de testes estruturado com critérios de aceite, cenários principais, casos de borda e sugestões de automação.

## Planejamento

O guia inicial do agente está em [docs/guia-geral-prompt.md](docs/guia-geral-prompt.md). Ele descreve o prompt-base, fluxo com LangGraph, estado recomendado, ferramenta integrada, validações e exemplos de entrada e saída.

## Base local de testes

O fluxo usa uma base local em [data/test_templates.md](data/test_templates.md) como referência controlada para critérios de aceite, cenários Given/When/Then, casos negativos, casos de borda e checklist de testabilidade.

A ferramenta de leitura permite apenas arquivos `.md` e `.txt` dentro da pasta `data/`, com limite de tamanho e erros controlados para caminhos inválidos, arquivos inexistentes, extensões não permitidas e arquivos grandes demais.

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

O ponto de entrada gera um plano de testes em Markdown com uma história padrão:

```bash
uv run test-plan-agent
```

Também é possível informar uma história pela linha de comando:

```bash
uv run test-plan-agent "Como cliente autenticado, quero consultar meus pedidos recentes para acompanhar a entrega."
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

Projeto com grafo LangGraph estruturado, leitura controlada da base local e geração determinística de plano de testes em Markdown.