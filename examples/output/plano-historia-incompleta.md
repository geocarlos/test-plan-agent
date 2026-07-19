# Plano de Testes

## Resumo da história
A exportação de relatórios precisa ser liberada

## Lacunas e ambiguidades
- Lacuna: A história deve indicar o ator ou perfil envolvido.
- Lacuna: A história deve indicar o resultado esperado ou valor gerado.

## Critérios de aceite verificáveis
- Dado que o ator descrito na história tem permissão para executar a ação, quando solicita o comportamento 'A exportação de relatórios precisa ser liberada', então o sistema deve apresentar o resultado esperado de forma observável.
- Dado que os dados necessários estão disponíveis, quando a ação principal é executada, então o sistema deve concluir o fluxo sem expor dados de outros usuários.
- Dado que não existem dados para exibir ou processar, quando o usuário executa a ação, então o sistema deve apresentar uma mensagem clara e verificável.

## Cenários principais em Given/When/Then
### Fluxo principal executado com sucesso
- Given: Dado que o usuário possui perfil válido e dados compatíveis com a regra de negócio
- When: Quando executa a ação descrita na história
- Then: Então o sistema apresenta o resultado esperado com informações completas e verificáveis

## Cenários alternativos e negativos
### Ausência de dados para a consulta ou operação
- Given: Dado que o usuário está autorizado, mas não possui registros aplicáveis
- When: Quando executa a ação descrita na história
- Then: Então o sistema informa que não há dados disponíveis sem gerar erro técnico

### Acesso sem autorização suficiente
- Given: Dado que o usuário não está autenticado ou não possui permissão adequada
- When: Quando tenta executar a ação descrita na história
- Then: Então o sistema bloqueia a operação e apresenta mensagem de acesso negado

## Casos de borda
- Executar o fluxo com exatamente um registro disponível.
- Executar o fluxo com volume alto de registros para verificar paginação, ordenação ou tempo de resposta definido.
- Verificar dados no limite de datas, valores, estados ou formatos aceitos pela regra de negócio.
- Validar comportamento quando dependências externas estiverem indisponíveis ou retornarem erro.

## Dados de exemplo
- Usuário válido: cliente_teste@example.com com perfil autorizado.
- Usuário inválido: visitante_sem_permissao@example.com sem acesso ao recurso.
- Entidade principal: registro 12345 com status ativo e data de referência 2026-07-18.
- Massa negativa: registro inexistente, campo obrigatório vazio e identificador em formato inválido.

## Sugestões de automação
- Automatizar o fluxo principal como teste de aceitação ou teste end-to-end.
- Criar testes de API ou serviço para permissões, estados vazios e erros esperados.
- Adicionar testes parametrizados para dados válidos, inválidos, mínimos e próximos aos limites.
- Manter cenários de ambiguidade como checklist manual até que as regras sejam objetivadas.

## Riscos e observações
- Contexto local usado: data/test_templates.md.
- Revisar critérios com pessoas de produto antes de transformar todos os cenários em automação definitiva.
- Prompt interno de formatação: Formate o plano final em Markdown com resumo, lacunas, critérios, cenários,
casos de borda, dados de exemplo, automação, riscos e observações.