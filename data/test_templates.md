# Templates e Exemplos de Testes

Base local de referência para apoiar a criação futura de planos de teste a partir de histórias de usuário, issues ou requisitos funcionais.

## Critérios de Aceite

Use critérios objetivos, verificáveis e ligados ao valor esperado pelo usuário.

Template:

```text
Dado que [contexto inicial]
Quando [ação ou evento]
Então [resultado observável esperado]
E [restrição, regra ou evidência adicional]
```

Exemplos:

- O usuário autenticado deve conseguir visualizar seus pedidos recentes com número, data, status e valor total.
- O sistema deve exibir uma mensagem clara quando não houver pedidos recentes.
- O resultado deve respeitar as permissões do usuário logado, sem expor dados de terceiros.

## Cenários Given/When/Then

Template principal:

```gherkin
Cenário: [nome do comportamento]
  Dado [estado inicial relevante]
  Quando [ação executada pelo usuário ou sistema]
  Então [resultado esperado verificável]
```

Exemplo:

```gherkin
Cenário: Consultar pedidos recentes com sucesso
  Dado que o cliente está autenticado
  E possui pedidos realizados nos últimos 90 dias
  Quando acessa a página de pedidos recentes
  Então o sistema exibe a lista de pedidos em ordem decrescente de data
  E cada pedido apresenta número, data, status e valor total
```

## Casos Negativos

Verifique falhas esperadas, permissões, entradas inválidas e dependências indisponíveis.

Exemplos:

- Usuário não autenticado tenta acessar o recurso.
- Usuário autenticado tenta acessar dados de outro usuário.
- Serviço externo necessário para consulta retorna erro.
- Entrada obrigatória está ausente, vazia ou em formato inválido.

## Casos de Borda

Explore limites de volume, datas, estados e combinações incomuns.

Exemplos:

- Usuário sem registros para exibir.
- Usuário com exatamente um registro.
- Usuário com grande volume de registros e paginação necessária.
- Datas no limite do período permitido.
- Status pouco frequentes, como cancelado, expirado ou em análise.

## Dados de Exemplo

Modelo simples:

```text
Usuário: cliente_teste@example.com
Perfil: cliente autenticado
Entidade principal: pedido 12345
Status esperado: em transporte
Data de referência: 2026-07-18
```

Inclua dados válidos, inválidos, mínimos e próximos aos limites definidos pela regra de negócio.

## Checklist de Testabilidade

- A regra de negócio está clara e possui resultado observável?
- Os critérios de aceite podem ser verificados por pessoa ou automação?
- Existem mensagens esperadas para falhas ou estados vazios?
- As permissões e restrições de acesso estão explícitas?
- Os dados necessários para executar os testes foram identificados?
- Há dependências externas, integrações ou riscos de indisponibilidade?
- Os limites de volume, data, formato e estado foram definidos?

## Riscos de Ambiguidade

- Termos como "recente", "rápido", "adequado" ou "completo" precisam de definição objetiva.
- Regras de ordenação, filtros e paginação devem ser descritas quando houver listas.
- Mensagens de erro devem ser verificáveis, não apenas "amigáveis".
- Regras de autorização devem indicar quem pode executar a ação e em quais condições.
