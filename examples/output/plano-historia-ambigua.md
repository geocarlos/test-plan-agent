# Plano de Testes

## Resumo da história
Como cliente, quero uma busca rápida e intuitiva para encontrar pedidos.

## Lacunas e ambiguidades
- O termo **“rápida”** precisa ser definido com uma métrica objetiva, como tempo máximo de resposta aceitável.
- O termo **“intuitiva”** precisa ser confirmado com critérios verificáveis, como quantidade máxima de passos, clareza dos rótulos ou taxa de sucesso na primeira tentativa.
- Não foi informado se a busca será por **número do pedido, data, status, produto, CPF/e-mail do cliente ou outros filtros**; confirmar com produto/negócio.
- Não foi especificado se a busca considera **somente pedidos do cliente logado** ou também pedidos de outros contextos; confirmar regra de acesso.
- Não foi definido se a funcionalidade possui **autocomplete, filtros, ordenação, paginação ou histórico de busca**; confirmar escopo.
- Não foi informada a mensagem esperada para **sem resultados** ou **erro de sistema**; confirmar texto e comportamento.

## Critérios de aceite verificáveis
- Dado que o cliente está autenticado e possui pedidos, quando realiza uma busca por um termo válido, então o sistema deve exibir apenas pedidos compatíveis com o termo informado.
- Dado que o cliente informa um critério de busca existente, quando executa a pesquisa, então os resultados devem ser exibidos em tempo aceitável a ser definido pelo produto/negócio.
- Dado que não existam pedidos compatíveis com o termo pesquisado, quando o cliente executar a busca, então o sistema deve exibir uma mensagem clara de “nenhum resultado encontrado” ou equivalente aprovada pelo produto.
- Dado que o cliente executa uma busca, quando os resultados forem exibidos, então os dados apresentados devem pertencer apenas ao cliente logado.
- Dado que a busca estiver indisponível por falha no sistema, quando o cliente tentar pesquisar, então o sistema deve apresentar uma mensagem de erro verificável e não expor detalhes técnicos.
- Dado que o cliente utiliza a busca, quando altera o termo pesquisado, então o sistema deve atualizar os resultados de forma coerente com o novo filtro informado.

## Cenários principais em Given/When/Then

### Cenário: Buscar pedidos com sucesso por número do pedido
```gherkin
Cenário: Buscar pedidos com sucesso por número do pedido
  Dado que o cliente está autenticado
  E possui pedidos cadastrados
  Quando informa um número de pedido existente na busca
  Então o sistema exibe o pedido correspondente
  E não exibe pedidos de outros clientes
```

### Cenário: Buscar pedidos com sucesso por termo parcial
```gherkin
Cenário: Buscar pedidos com sucesso por termo parcial
  Dado que o cliente está autenticado
  E possui pedidos com informações compatíveis com o termo parcial
  Quando informa parte de um identificador ou descrição permitida na busca
  Então o sistema exibe os pedidos compatíveis com o termo
  E mantém a ordenação definida pela regra de negócio, se aplicável
```

### Cenário: Buscar pedidos e visualizar lista de resultados
```gherkin
Cenário: Buscar pedidos e visualizar lista de resultados
  Dado que o cliente está autenticado
  E possui múltiplos pedidos compatíveis com a busca
  Quando executa a pesquisa
  Então o sistema exibe a lista de pedidos encontrados
  E cada item apresenta as informações definidas pelo produto/negócio
```

### Cenário: Buscar pedidos sem resultado
```gherkin
Cenário: Buscar pedidos sem resultado
  Dado que o cliente está autenticado
  E não possui pedidos compatíveis com o termo pesquisado
  Quando executa a pesquisa
  Então o sistema exibe uma mensagem de nenhum resultado encontrado
  E não apresenta erro técnico
```

## Cenários alternativos e negativos

### Cenário: Cliente não autenticado tenta buscar pedidos
```gherkin
Cenário: Cliente não autenticado tenta buscar pedidos
  Dado que o usuário não está autenticado
  Quando tenta acessar ou executar a busca de pedidos
  Então o sistema deve bloquear o acesso
  E exibir orientação para autenticação, conforme regra do produto
```

### Cenário: Cliente busca com termo inválido
```gherkin
Cenário: Cliente busca com termo inválido
  Dado que o cliente está autenticado
  Quando informa um termo vazio ou inválido
  Então o sistema deve impedir a execução da busca ou exibir validação adequada
  E a mensagem deve ser clara e verificável
```

### Cenário: Falha na consulta de pedidos
```gherkin
Cenário: Falha na consulta de pedidos
  Dado que o cliente está autenticado
  E o serviço de consulta de pedidos está indisponível
  Quando executa a busca
  Então o sistema exibe mensagem de indisponibilidade
  E não expõe stack trace, código interno ou detalhe técnico
```

### Cenário: Cliente tenta acessar pedidos de outro usuário
```gherkin
Cenário: Cliente tenta acessar pedidos de outro usuário
  Dado que o cliente está autenticado
  Quando tenta pesquisar ou visualizar um pedido que não pertence à sua conta
  Então o sistema deve negar o acesso
  E não deve revelar informação sensível de terceiros
```

## Casos de borda
- Buscar com **exatamente um pedido** compatível.
- Buscar com **muitos pedidos** compatíveis, verificando paginação ou carregamento incremental, se existir.
- Buscar com **termo muito curto** ou mínimo permitido.
- Buscar com **termo muito longo**, validando limite de caracteres.
- Buscar com **caracteres especiais**, acentos, maiúsculas/minúsculas e espaços extras.
- Buscar em um cenário de **nenhum pedido cadastrado**.
- Buscar com **rede lenta** ou resposta do serviço acima do tempo esperado.
- Buscar com **datas limite** se a pesquisa permitir filtros por período.
- Buscar com pedidos em **estados diferentes** como cancelado, entregue, em transporte ou processando, se aplicável.
- Buscar repetidamente em curto intervalo, verificando **consistência de resposta** e ausência de duplicidade de resultados.

## Dados de exemplo
- Cliente válido: `cliente_teste@example.com`
- Cliente sem permissão: `usuario_sem_acesso@example.com`
- Pedido existente: `PED-12345`
- Pedido inexistente: `PED-99999`
- Termo de busca válido: `12345`
- Termo parcial: `PED-12`
- Termo inválido: string vazia ou apenas espaços
- Status de pedido: `em transporte`
- Data de referência: `2026-07-18`

## Sugestões de automação
- Automatizar os cenários principais como **testes E2E** da busca de pedidos.
- Criar testes de **API/serviço** para validação de filtros, permissões, ausência de resultados e falhas de integração.
- Usar **testes parametrizados** para variações de termos válidos, inválidos, limites de tamanho e caracteres especiais.
- Incluir verificação de **tempo de resposta**, desde que o produto/negócio defina a métrica aceitável.
- Manter os cenários com ambiguidade de escopo como **checklist manual** até a confirmação das regras de busca.

## Riscos e observações
- A história contém termos subjetivos como **“rápida”** e **“intuitiva”**, que precisam ser convertidos em critérios mensuráveis para evitar divergência na validação.
- Sem definição do escopo de busca, há risco de testes cobrirem campos além do esperado ou deixarem de validar campos relevantes.
- É importante confirmar se a busca deve respeitar **paginação, ordenação e filtros adicionais**.
- Mensagens de vazio e erro devem ser aprovadas por produto/negócio para garantir verificabilidade.
- O contexto local usado como referência foi `data/test_templates.md`, priorizando estrutura objetiva, cenários Given/When/Then e cobertura de casos negativos e de borda.
