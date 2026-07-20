# Plano de Testes

## Resumo da história
Como cliente autenticado, quero consultar meus pedidos recentes para acompanhar o status de entrega.

## Lacunas e ambiguidades
- A história não define o que significa “recentes” em termos de período, quantidade ou ordenação.
- Não foi informado se a consulta será em tela, API ou ambos.
- Não foram explicitadas regras de paginação, filtros, ordenação e campos obrigatórios de exibição.
- Não foi definido se pedidos cancelados, devolvidos ou em análise entram no conjunto de “recentes”.
- Precisa ser confirmado com produto/negócio se haverá mensagem específica para ausência de pedidos.

## Critérios de aceite verificáveis
- Dado que o cliente está autenticado, quando consultar seus pedidos recentes, então o sistema deve exibir apenas pedidos do próprio cliente.
- Dado que existirem pedidos recentes, quando a consulta for executada, então o sistema deve mostrar uma lista com informações verificáveis dos pedidos.
- Dado que a regra de negócio estiver definida para “recentes”, quando a lista for exibida, então a ordenação e o período considerado devem seguir exatamente essa regra.
- Dado que não houver pedidos recentes, quando o cliente consultar a lista, então o sistema deve apresentar uma mensagem clara de ausência de pedidos.
- Dado que o cliente não estiver autenticado, quando tentar acessar a consulta, então o sistema deve bloquear o acesso.
- Dado que houver pedidos de outros clientes, quando a consulta for feita, então esses dados não devem ser exibidos.

## Cenários principais em Given/When/Then
### Consultar pedidos recentes com sucesso
```gherkin
Cenário: Consultar pedidos recentes com sucesso
  Dado que o cliente está autenticado
  E possui pedidos dentro do período considerado recente
  Quando acessa a área de pedidos recentes
  Então o sistema exibe a lista de pedidos do próprio cliente
  E cada pedido apresenta número, data, status e valor total
```

### Exibir status de entrega do pedido
```gherkin
Cenário: Visualizar status de entrega de um pedido recente
  Dado que o cliente está autenticado
  E possui pelo menos um pedido recente com status de entrega disponível
  Quando consulta seus pedidos recentes
  Então o sistema exibe o status de entrega correspondente a cada pedido
```

### Manter isolamento entre usuários
```gherkin
Cenário: Não exibir pedidos de outros clientes
  Dado que o cliente está autenticado
  E existem pedidos associados a outros clientes no sistema
  Quando consulta seus pedidos recentes
  Então o sistema exibe somente pedidos vinculados ao cliente logado
  E não apresenta dados de terceiros
```

## Cenários alternativos e negativos
### Cliente autenticado sem pedidos recentes
```gherkin
Cenário: Exibir mensagem quando não houver pedidos recentes
  Dado que o cliente está autenticado
  E não possui pedidos dentro do período considerado recente
  Quando consulta seus pedidos recentes
  Então o sistema exibe uma mensagem clara informando que não há pedidos recentes
```

### Cliente não autenticado tenta acessar a consulta
```gherkin
Cenário: Bloquear acesso sem autenticação
  Dado que o usuário não está autenticado
  Quando tenta acessar a consulta de pedidos recentes
  Então o sistema bloqueia o acesso
  E exibe orientação para autenticação
```

### Cliente tenta acessar pedidos de outro usuário
```gherkin
Cenário: Impedir acesso a pedidos de terceiros
  Dado que o cliente está autenticado
  Quando tenta acessar um pedido que não pertence à sua conta
  Então o sistema não exibe os dados do pedido
  E retorna uma resposta de acesso negado ou recurso não encontrado, conforme regra definida
```

### Dependência indisponível na consulta
```gherkin
Cenário: Tratar indisponibilidade ao consultar pedidos
  Dado que o cliente está autenticado
  E a dependência responsável pela consulta está indisponível
  Quando solicita seus pedidos recentes
  Então o sistema exibe uma mensagem de erro controlada
  E não mostra informação incompleta ou inconsistente
```

## Casos de borda
- Cliente com exatamente um pedido recente.
- Cliente com grande volume de pedidos recentes, verificando desempenho e paginação.
- Pedido com status pouco frequente, como cancelado, devolvido ou em análise, conforme regra permitida.
- Consulta no limite do período definido para considerar um pedido como recente.
- Lista vazia com cliente autenticado e sem pedidos no intervalo esperado.
- Pedido com data de criação muito próxima à data de referência do teste.
- Ordenação em caso de múltiplos pedidos com mesma data.
- Falha temporária da dependência de dados durante a consulta.

## Dados de exemplo
- Cliente válido: cliente_teste@example.com
- Perfil: cliente autenticado
- Pedido recente 1: pedido 10001, data 2026-07-18, status em transporte, valor total 149,90
- Pedido recente 2: pedido 10002, data 2026-07-17, status entregue, valor total 89,50
- Pedido fora do período: pedido 09999, data 2025-12-01, status entregue, valor total 59,90
- Massa negativa: pedido inexistente, pedido de outro cliente, usuário não autenticado
- Data de referência: 2026-07-18

## Sugestões de automação
- Automatizar o fluxo principal como teste E2E ou de aceitação.
- Cobrir autenticação e autorização com testes de API, quando aplicável.
- Criar testes parametrizados para:
  - com pedidos recentes;
  - sem pedidos recentes;
  - acesso sem autenticação;
  - tentativa de acesso a dados de terceiros.
- Validar campos exibidos e ordenação com asserções objetivas.
- Manter cenários sobre definição de “recentes” automatizados apenas após confirmação da regra de negócio.
- Incluir verificação de paginação e limite de volume se a consulta retornar listas extensas.

## Riscos e observações
- A expressão “pedidos recentes” precisa de definição objetiva para evitar divergência entre desenvolvimento, testes e negócio.
- Sem regra explícita de ordenação, o comportamento pode variar entre implementações.
- A ausência de definição sobre paginação pode impactar usabilidade e desempenho em listas grandes.
- Mensagens de erro e de estado vazio devem ser validadas com o time de produto para garantir consistência.
- Este plano foi elaborado com base na história informada e no template local de referência `data/test_templates.md`.
- Antes de automatizar completamente, confirmar: período de “recente”, campos obrigatórios, regras de status e resposta esperada para autenticação/autorização.
