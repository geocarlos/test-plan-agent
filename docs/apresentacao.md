---
marp: true
theme: default
paginate: true
size: 16:9
---

<style>
section {
	--ink: #172033;
	--muted: #5f6b7a;
	--brand: #2457d6;
	--brand-2: #00a884;
	--warn: #f59e0b;
	--paper: #f8fafc;
	--line: #d7deea;
	background: linear-gradient(135deg, #f8fafc 0%, #edf4ff 48%, #f3fbf6 100%);
	color: var(--ink);
	font-family: "Aptos", "Segoe UI", sans-serif;
	padding: 44px 56px;
}

h1 {
	color: var(--brand);
	font-size: 44px;
	margin: 0 0 10px;
}

h2 {
	color: var(--ink);
	font-size: 25px;
	margin: 0 0 18px;
}

p,
li {
	font-size: 21px;
	line-height: 1.35;
}

strong {
	color: var(--brand);
}

.eyebrow {
	color: var(--brand-2);
	font-size: 17px;
	font-weight: 700;
	letter-spacing: .08em;
	text-transform: uppercase;
}

.layout {
	align-items: center;
	display: grid;
	gap: 34px;
	grid-template-columns: .9fr 1.1fr;
}

.layout.compact {
	gap: 28px;
	grid-template-columns: .78fr 1.22fr;
}

.panel {
	background: rgba(255, 255, 255, .78);
	border: 1px solid var(--line);
	border-radius: 14px;
	box-shadow: 0 18px 45px rgba(36, 87, 214, .12);
	padding: 24px;
}

.chips {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
	margin-top: 18px;
}

.chip {
	background: #fff;
	border: 1px solid var(--line);
	border-left: 5px solid var(--brand-2);
	border-radius: 999px;
	color: var(--ink);
	font-size: 16px;
	font-weight: 700;
	padding: 8px 13px;
}

.diagram {
	background: rgba(255, 255, 255, .82);
	border: 1px solid var(--line);
	border-radius: 16px;
	padding: 18px;
}

.layout.compact .diagram {
	border-radius: 12px;
	padding: 12px;
}

.diagram img {
	display: block;
	height: auto;
}

footer {
	color: var(--muted);
	font-size: 14px;
}

.summary-list {
	display: grid;
	gap: 12px;
	margin-top: 20px;
}

.summary-list div {
	background: rgba(255, 255, 255, .82);
	border: 1px solid var(--line);
	border-left: 5px solid var(--brand-2);
	border-radius: 12px;
	font-size: 18px;
	line-height: 1.28;
	padding: 12px 14px;
}

.summary-list strong {
	display: block;
	font-size: 15px;
	letter-spacing: .06em;
	margin-bottom: 4px;
	text-transform: uppercase;
}
</style>

<div class="layout">
<div>

<div class="eyebrow">Mini-projeto avaliativo</div>

# Test-Plan Agent

## Planejamento de testes a partir de histórias de usuário

Histórias de usuário chegam com lacunas, ambiguidade e poucos critérios verificáveis. O agente automatiza a primeira análise de testabilidade e devolve um plano objetivo para QA e desenvolvimento.

<div class="summary-list">
	<div><strong>Proposta</strong>Transformar requisitos em critérios de aceite, cenários, riscos e sugestões de automação.</div>
	<div><strong>Entrada</strong>História de usuário, issue ou requisito funcional, por argumento ou arquivo Markdown.</div>
	<div><strong>Saída</strong>Plano de testes estruturado em Markdown.</div>
</div>

</div>
<div class="diagram">
	<img width="100%" src="assets/apresentacao-overview.svg" alt="Visão geral do Test-Plan Agent" />
</div>
</div>

---

<div class="layout compact">
<div>

<div class="eyebrow">Ferramenta e fluxo</div>

# Como o agente funciona

## Fluxo com LangGraph, contexto local e geração final

<div class="summary-list">
	<div><strong>Processo automatizado</strong>Validar a história, buscar contexto, identificar lacunas e montar o plano de testes.</div>
	<div><strong>Ferramenta</strong>Leitura controlada de <code>data/test_templates.md</code>, restrita à pasta <code>data/</code>.</div>
	<div><strong>Geração</strong>Usa LLM quando configurado; sem configuração, usa fallback determinístico explícito.</div>
</div>

<div class="chips">
	<span class="chip">Validação</span>
	<span class="chip">Contexto</span>
	<span class="chip">Plano final</span>
</div>

</div>
<div class="diagram">
	<img width="70%" src="assets/apresentacao-flow.svg" alt="Fluxo de execução do agente" />
</div>
</div>
