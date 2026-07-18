# Guia geral de planejamento do Test-Plan Agent

Este documento funciona como um prompt-guia para orientar a concepcao, implementacao e validacao do **Test-Plan Agent**, um agente com LangGraph que transforma historias de usuario em planos de teste verificaveis.

## Contexto do projeto

O agente deve apoiar desenvolvedores, pessoas de QA e estudantes na traducao de requisitos funcionais em criterios de aceite, cenarios de teste, casos negativos, casos de borda, dados de exemplo e riscos de ambiguidade.

A entrada principal sera uma historia de usuario, issue ou requisito funcional em texto livre. A saida principal sera um plano de testes estruturado, claro e testavel.

## Objetivo do agente

Receber uma historia de usuario e gerar um plano de testes contendo:

- criterios de aceite objetivos;
- cenarios principais em formato Given/When/Then;
- cenarios alternativos e negativos;
- casos de borda relevantes;
- dados de exemplo para execucao dos testes;
- riscos, lacunas e ambiguidades do requisito;
- sugestoes de automacao quando fizer sentido.

## Prompt-guia

Use o prompt abaixo como base para planejar ou implementar o comportamento do agente:

```text
Voce e um agente planejador de testes para times de desenvolvimento de software.

Sua tarefa e receber uma historia de usuario, issue ou requisito funcional e transformar esse texto em um plano de testes verificavel.

Antes de gerar a resposta final, valide se a entrada possui pelo menos:
- um ator ou usuario interessado;
- uma acao, necessidade ou objetivo;
- um resultado esperado, beneficio ou valor de negocio.

Se a entrada for muito curta, vaga ou incompleta, sinalize as lacunas antes de propor testes. Nao invente regras de negocio especificas sem marcar claramente como suposicao.

Use uma base local de exemplos e templates de criterios de aceite como contexto auxiliar. Aplique os exemplos apenas quando forem relevantes para a historia recebida.

Gere uma resposta final em Markdown com as secoes:
1. Resumo da historia
2. Lacunas e ambiguidades
3. Criterios de aceite verificaveis
4. Cenarios principais em Given/When/Then
5. Cenarios alternativos e negativos
6. Casos de borda
7. Dados de exemplo
8. Sugestoes de automacao
9. Riscos e observacoes

Cada criterio de aceite deve ser objetivo e testavel. Evite termos vagos como "rapido", "facil", "adequado" ou "intuitivo" sem uma metrica ou condicao observavel.

Para cada cenario de teste, descreva:
- Given: estado inicial ou pre-condicao;
- When: acao executada pelo usuario ou sistema;
- Then: resultado esperado verificavel.

Ao final, informe se o requisito esta pronto para planejamento de testes ou se precisa de refinamento antes da implementacao.
```

## Fluxo sugerido com LangGraph

```text
Entrada da historia de usuario
↓
Validacao da entrada
↓
Carregamento de templates e exemplos locais
↓
Analise de lacunas e ambiguidade
↓
Geracao de criterios de aceite
↓
Geracao de cenarios de teste
↓
Validacao de testabilidade
↓
Resposta final em Markdown
```

## Estado recomendado

O estado compartilhado do LangGraph pode conter os seguintes campos:

```python
class TestPlanState(TypedDict):
    user_story: str
    is_valid: bool
    validation_errors: list[str]
    templates_context: str
    gaps: list[str]
    acceptance_criteria: list[str]
    test_scenarios: list[dict]
    edge_cases: list[str]
    example_data: list[dict]
    automation_suggestions: list[str]
    final_answer: str
```

## Nos do grafo

- `validate_input`: verifica tamanho minimo, presenca de ator, objetivo e resultado esperado.
- `load_test_templates`: usa uma ferramenta local para ler templates e exemplos em `data/test_templates.md`.
- `analyze_story`: identifica lacunas, ambiguidades, entidades e regras implicitas.
- `generate_acceptance_criteria`: produz criterios de aceite objetivos e verificaveis.
- `generate_test_scenarios`: cria cenarios principais, alternativos, negativos e casos de borda.
- `validate_testability`: marca criterios ou cenarios que nao possam ser testados objetivamente.
- `format_final_answer`: monta a resposta final em Markdown.

## Ferramenta integrada

A ferramenta principal deve ler uma base local de templates e exemplos, por exemplo:

```text
data/test_templates.md
```

Essa base pode conter:

- modelo de criterio de aceite;
- exemplos de Given/When/Then;
- exemplos de casos negativos;
- exemplos de casos de borda;
- checklist de testabilidade.

Regras de seguranca da ferramenta:

- permitir leitura apenas dentro da pasta `data/`;
- aceitar apenas arquivos `.md` ou `.txt`;
- limitar tamanho maximo do arquivo lido;
- retornar erro controlado quando o arquivo nao existir;
- nao ler `.env`, credenciais ou arquivos fora do projeto.

## Validacoes basicas

O agente deve rejeitar ou sinalizar entradas que tenham:

- menos de 40 caracteres;
- ausencia clara de ator;
- ausencia clara de objetivo ou acao;
- ausencia clara de resultado esperado;
- requisito com multiplas funcionalidades misturadas sem separacao;
- termos subjetivos sem metrica observavel.

Exemplos de termos que exigem alerta:

- "rapido";
- "simples";
- "intuitivo";
- "seguro";
- "melhor";
- "adequado".

## Exemplo de entrada

```text
Como cliente de uma loja online, quero recuperar minha senha por e-mail para voltar a acessar minha conta quando esquecer minhas credenciais.
```

## Exemplo de saida esperada

```markdown
## Resumo da historia

Cliente de uma loja online deseja recuperar a senha por e-mail para voltar a acessar a conta.

## Lacunas e ambiguidades

- Nao informa prazo de expiracao do link de recuperacao.
- Nao informa se deve haver limite de tentativas.
- Nao informa mensagem esperada para e-mails nao cadastrados.

## Criterios de aceite verificaveis

1. Dado um e-mail cadastrado, quando o cliente solicitar recuperacao de senha, entao o sistema deve enviar um e-mail com link de redefinicao.
2. Dado um link de redefinicao valido, quando o cliente cadastrar uma nova senha valida, entao a senha deve ser atualizada.
3. Dado um e-mail nao cadastrado, quando o cliente solicitar recuperacao, entao o sistema deve exibir uma mensagem generica sem revelar se o e-mail existe.

## Cenarios principais em Given/When/Then

### Recuperacao com e-mail cadastrado

Given que existe uma conta ativa com o e-mail cliente@exemplo.com
When o cliente solicita recuperacao de senha para esse e-mail
Then o sistema envia um e-mail com link de redefinicao

## Cenarios alternativos e negativos

- Solicitar recuperacao com e-mail em formato invalido.
- Usar link de recuperacao expirado.
- Tentar cadastrar senha que nao atende a politica minima.

## Casos de borda

- Solicitar recuperacao varias vezes em sequencia.
- Abrir o mesmo link apos a senha ja ter sido alterada.
- Informar e-mail com letras maiusculas e minusculas misturadas.

## Dados de exemplo

| Caso | E-mail | Resultado esperado |
| --- | --- | --- |
| Conta existente | cliente@exemplo.com | E-mail de recuperacao enviado |
| E-mail invalido | cliente@ | Erro de validacao exibido |
| Conta inexistente | desconhecido@exemplo.com | Mensagem generica exibida |

## Sugestoes de automacao

- Teste de API para solicitacao de recuperacao de senha.
- Teste de integracao para validacao do token de redefinicao.
- Teste end-to-end cobrindo fluxo completo de troca de senha.

## Riscos e observacoes

- A historia precisa definir expiracao do link e politica de senha.
- O fluxo deve evitar vazamento de informacao sobre e-mails cadastrados.
```

## Criterios de pronto para o mini-projeto

O projeto deve evidenciar:

- uso de `StateGraph` do LangGraph;
- estado compartilhado com entrada, validacoes, contexto, criterios, cenarios e resposta final;
- ferramenta real para leitura de base local de templates;
- validacao de entrada e limites de seguranca;
- exemplos de entrada e saida;
- README com problema, objetivo, fluxo, execucao, ferramenta e limitacoes;
- registro dos prompts usados durante o desenvolvimento.
