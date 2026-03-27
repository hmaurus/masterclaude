---
name: aicflow-marketing-analytics
description: "Esta skill deve ser usada quando o usuário pedir para analisar dados de marketing, leads, compras, receita, SEO, PageSpeed, Core Web Vitals, tráfego ou conversões dos sites aicodingflow.com e masterclaude.com. Ativa para consultas sobre Stripe, Google Search Console, GA4, Ahrefs, Moz, SEMrush, domain authority, backlinks, funil de conversão, checkouts abandonados. Também aplicável para perguntas simples como 'quantos leads temos?', 'como estão as vendas?', 'relatório de marketing', 'performance do site', 'dashboard de métricas', 'KPIs do mês'."
---

# AICFlow Marketing Analytics

Skill especialista em buscar, analisar e reportar dados de marketing dos sites aicodingflow.com e masterclaude.com.

## Contexto do Projeto

Dois domínios servidos pelo mesmo app Next.js:
- **aicodingflow.com** — produto principal (Guide freemium + Curso)
- **masterclaude.com** — portal de conteúdo editorial (~60 artigos)

Produtos monetizados:
- **Guide** (Claude Code Guide) — freemium, plano pago em BRL e USD
- **Curso** (Criador de Apps com Claude Code) — plano anual e lifetime

## Fontes de Dados

Consultar `references/data-sources.md` para instruções detalhadas de acesso a cada fonte.

| Fonte | Tipo de Dado | Acesso |
|-------|-------------|--------|
| PostgreSQL (Prisma) | Leads, compras, usuários, email enrollments | psql ou Prisma Studio |
| Stripe CLI/API | Receita, pagamentos, checkouts abandonados | `stripe` CLI |
| PageSpeed Insights | Core Web Vitals, performance, SEO score | API HTTP (gratuita) |
| Google Search Console | Impressões, cliques, CTR, posição média | Interface web ou API |
| Google Analytics (GA4) | Tráfego, pageviews, sessões, conversões | Interface web ou API |
| Google Ads | Conversões, CPC, impressões de anúncios | Interface web |
| SEMrush / Ahrefs / Moz | Domain authority, backlinks, keywords | Interface web ou API |

## Workflow de Análise

### 1. Identificar a Pergunta

Determinar o que o usuário quer saber. Categorias comuns:

- **Leads & Conversão**: quantos leads, taxa de conversão, fontes de tráfego
- **Receita & Compras**: faturamento, ticket médio, checkouts abandonados
- **SEO & Busca**: posição no Google, impressões, backlinks, domain authority
- **Performance Técnica**: PageSpeed, Core Web Vitals, tempo de carregamento
- **Conteúdo**: páginas mais acessadas, artigos mais lidos, engajamento
- **Email Marketing**: taxa de abertura, enrollments ativos, sequências

### 2. Coletar Dados

Para cada categoria, usar a fonte apropriada:

**Dados internos (DB + Stripe):** Executar queries SQL ou comandos Stripe CLI. Ver scripts disponíveis em `scripts/`.

```bash
# Relatório completo de leads e compras
bash ${CLAUDE_PLUGIN_ROOT}/skills/marketing-analytics/scripts/db-marketing-report.sh

# Relatório de PageSpeed + Core Web Vitals
bash ${CLAUDE_PLUGIN_ROOT}/skills/marketing-analytics/scripts/pagespeed-report.sh https://aicodingflow.com
bash ${CLAUDE_PLUGIN_ROOT}/skills/marketing-analytics/scripts/pagespeed-report.sh https://masterclaude.com
```

**Dados Stripe (receita, checkouts):**

```bash
# Pagamentos recentes
stripe payments list --limit 20

# Checkouts expirados (quase compras)
stripe checkout sessions list --status expired --limit 20

# Balanço do mês
stripe balance transactions list --created[gte]=$(date -d "first day of this month" +%s) --limit 100
```

**Dados externos (SEO, Search Console):** Usar WebFetch para APIs gratuitas ou orientar o usuário a consultar interfaces web para ferramentas pagas.

### 3. Analisar e Reportar

Consultar `references/kpis-benchmarks.md` para definições de KPIs e benchmarks SaaS de referência.

Ao apresentar resultados:
- Comparar com períodos anteriores quando possível (WoW, MoM)
- Destacar tendências positivas e alertas
- Incluir benchmarks de mercado para contextualizar
- Sugerir ações concretas baseadas nos dados
- Formatar com tabelas e listas para facilitar leitura

### 4. Formato do Relatório

Estruturar relatórios com seções claras:

```
## Relatório de Marketing — [Período]

### Resumo Executivo
[2-3 bullet points com highlights]

### Leads & Conversão
[Dados + análise]

### Receita
[Dados + análise]

### SEO & Tráfego
[Dados + análise]

### Performance Técnica
[Dados + análise]

### Recomendações
[Ações sugeridas ordenadas por impacto]
```

## Scripts Disponíveis

| Script | Propósito |
|--------|-----------|
| `scripts/db-marketing-report.sh` | Relatório completo de leads, compras, usuários e email enrollments do PostgreSQL |
| `scripts/pagespeed-report.sh` | Coleta e formata PageSpeed Insights + Core Web Vitals para uma URL |

## Fallbacks e Troubleshooting

Se uma fonte de dados não estiver disponível:
- **SSH falha**: verificar conexão VPS (`ssh mh-vps`) e status do container (`docker ps`)
- **Stripe CLI não autenticado**: executar `stripe login` antes dos comandos
- **PageSpeed API com erro**: verificar URL (deve incluir protocolo) e tentar novamente
- **Ferramentas pagas (Ahrefs/Moz/SEMrush)**: orientar o usuário a acessar a interface web manualmente
- **GA4/Search Console sem API**: orientar o usuário a consultar a interface web e compartilhar screenshots

Para queries SQL prontas e instruções de acesso ao banco de dados, consultar `references/data-sources.md` seção "Queries Essenciais".

Para thresholds de Core Web Vitals e alvos Lighthouse, consultar `references/kpis-benchmarks.md` seção "KPIs de Performance Técnica".

## Referências

- **`references/data-sources.md`** — Guia detalhado de acesso a cada fonte de dados
- **`references/kpis-benchmarks.md`** — Definições de KPIs e benchmarks SaaS para comparação
