# Fontes de Dados — Guia de Acesso

Guia detalhado para acessar cada fonte de dados de marketing do aicodingflow.com e masterclaude.com.

---

## 1. PostgreSQL (Banco de Dados Interno)

O banco de dados do projeto é a fonte primária para leads, compras, usuários e email marketing.

### Schema Relevante

**Lead** (`leads`):
- `email`, `product` (guide/curso), `source` (checkout/newsletter/popup)
- `utm_source`, `utm_medium`, `utm_campaign` — rastreamento de origem
- `converted` (boolean) — indica se virou compra
- `created_at` — data de captura

**Purchase** (`purchases`):
- `user_id`, `product`, `plan`, `currency` (BRL/USD)
- `amount_paid` (em centavos), `status` (completed)
- `stripe_session_id`, `stripe_payment_intent`
- `expires_at` — para planos com expiração
- `created_at` — data da compra

**User** (`users`):
- `email`, `name`, `role`, `stripe_customer_id`
- `email_verified`, `created_at`

**EmailEnrollment** (`email_enrollments`):
- `email`, `sequence_id`, `current_step`
- `status` (active/completed/cancelled)
- `next_send_at`

**GuideProgress** (`guide_progress`):
- `user_id`, `section_slug`, `completed_at`

### Acesso

**Produção (via SSH na VPS):**
```bash
# Query interativa
ssh mh-vps "docker exec -it aicodingflow-db psql -U aicodingflow -d aicodingflow"

# Query não-interativa (piping)
ssh mh-vps "docker exec -i aicodingflow-db psql -U aicodingflow -d aicodingflow -c 'SELECT COUNT(*) FROM leads;'"
```

**Local (desenvolvimento):**
```bash
# Ler DATABASE_URL do .env
source <(grep DATABASE_URL /home/mh/dev/aicodingflow/.env)
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM leads;"
```

### Queries Essenciais

```sql
-- Dashboard rápido
SELECT
  (SELECT COUNT(*) FROM leads) as total_leads,
  (SELECT COUNT(*) FROM leads WHERE converted = true) as leads_convertidos,
  (SELECT COUNT(*) FROM purchases WHERE status = 'completed') as total_compras,
  (SELECT COUNT(*) FROM users) as total_usuarios,
  (SELECT COUNT(*) FROM email_enrollments WHERE status = 'active') as emails_ativos;

-- Funil de conversão por produto
SELECT
  product,
  COUNT(*) as leads,
  SUM(CASE WHEN converted THEN 1 ELSE 0 END) as convertidos,
  ROUND(100.0 * SUM(CASE WHEN converted THEN 1 ELSE 0 END) / COUNT(*), 1) as taxa_conversao
FROM leads
GROUP BY product;

-- Receita mensal
SELECT
  DATE_TRUNC('month', created_at) as mes,
  product,
  currency,
  COUNT(*) as vendas,
  SUM(amount_paid) / 100.0 as receita
FROM purchases
WHERE status = 'completed'
GROUP BY mes, product, currency
ORDER BY mes DESC;

-- Leads por dia (últimos 30 dias)
SELECT
  DATE(created_at) as dia,
  product,
  source,
  COUNT(*) as novos
FROM leads
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY dia, product, source
ORDER BY dia DESC;

-- Top UTM campaigns
SELECT
  utm_source, utm_medium, utm_campaign,
  COUNT(*) as leads,
  SUM(CASE WHEN converted THEN 1 ELSE 0 END) as convertidos
FROM leads
WHERE utm_source IS NOT NULL
GROUP BY utm_source, utm_medium, utm_campaign
ORDER BY leads DESC
LIMIT 20;

-- Checkouts abandonados (quase compras)
SELECT
  product,
  DATE(created_at) as dia,
  COUNT(*) as abandonados
FROM leads
WHERE source = 'checkout' AND converted = false
GROUP BY product, dia
ORDER BY dia DESC;

-- Progresso no Guide (engajamento)
SELECT
  section_slug,
  COUNT(DISTINCT user_id) as usuarios,
  MIN(completed_at) as primeira_conclusao,
  MAX(completed_at) as ultima_conclusao
FROM guide_progress
GROUP BY section_slug
ORDER BY usuarios DESC;

-- Email sequences - status
SELECT
  e.sequence_id,
  s.name as sequence_name,
  e.status,
  COUNT(*) as total,
  AVG(e.current_step) as step_medio
FROM email_enrollments e
LEFT JOIN email_sequences s ON e.sequence_id = s.id
GROUP BY e.sequence_id, s.name, e.status;
```

---

## 2. Stripe

Stripe é usado para pagamentos de Guide e Curso. Acesso via CLI ou API.

### Stripe CLI

```bash
# Listar pagamentos recentes
stripe payments list --limit 20

# Filtrar por status
stripe payments list --status succeeded --limit 50

# Checkouts expirados (quase compras / abandonados)
stripe checkout sessions list --status expired --limit 20

# Checkouts completos
stripe checkout sessions list --status complete --limit 20

# Balanço de transações do mês atual
stripe balance transactions list \
  --created[gte]=$(date -d "first day of this month" +%s) \
  --limit 100

# Detalhes de um cliente
stripe customers retrieve cus_xxx

# Listar produtos e preços
stripe products list
stripe prices list

# Eventos recentes (webhooks)
stripe events list --limit 20
```

### Métricas Stripe Importantes

- **MRR** (Monthly Recurring Revenue): Não aplicável diretamente (one-time purchases)
- **Receita bruta**: soma de `amount_paid` das purchases
- **Ticket médio**: receita / número de vendas
- **Taxa de abandono**: checkouts expirados / (expirados + completos)
- **Receita por produto**: guide vs curso
- **Receita por moeda**: BRL vs USD

### IDs de Preço

Os preços estão configurados em variáveis de ambiente:
- `STRIPE_PRICE_CURSO_ANNUAL` — Curso plano anual
- `STRIPE_PRICE_CURSO_LIFETIME` — Curso plano lifetime
- `STRIPE_PRICE_GUIDE_BRL` — Guide em BRL
- `STRIPE_PRICE_GUIDE_USD` — Guide em USD

---

## 3. Google Analytics (GA4)

Dois GA4 properties configurados:
- `NEXT_PUBLIC_GA_ID_AICODINGFLOW` — aicodingflow.com
- `NEXT_PUBLIC_GA_ID_MASTERCLAUDE` — masterclaude.com

### Acesso

**Interface web:** https://analytics.google.com/

**API (GA4 Data API):**
```bash
# Requer autenticação OAuth2 ou Service Account
# Endpoint: https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport
```

### Métricas Relevantes

- **Sessões e Usuários**: tráfego total, novos vs recorrentes
- **Pageviews**: páginas mais acessadas
- **Bounce Rate**: taxa de rejeição por página
- **Duração média da sessão**: engajamento
- **Fontes de tráfego**: organic, direct, social, referral, paid
- **Conversões**: eventos configurados (checkout, signup)
- **Geolocalização**: distribuição de visitantes por país/região

### Relatórios Úteis

1. **Aquisição > Visão geral**: de onde vem o tráfego
2. **Engajamento > Páginas e telas**: páginas mais acessadas
3. **Monetização > Visão geral**: receita e transações (se configurado)
4. **Público > Dados demográficos**: perfil dos visitantes

---

## 4. Google Search Console

Monitoramento de presença na busca do Google.

### Acesso

**Interface web:** https://search.google.com/search-console/

**Propriedades:**
- `https://aicodingflow.com/`
- `https://masterclaude.com/`

### Métricas Disponíveis

- **Impressões**: quantas vezes o site apareceu na busca
- **Cliques**: quantas vezes foi clicado
- **CTR** (Click-Through Rate): cliques / impressões
- **Posição média**: posição média nos resultados
- **Queries**: termos de busca que levam ao site
- **Páginas**: quais páginas recebem tráfego orgânico
- **Dispositivos**: mobile vs desktop
- **Países**: distribuição geográfica

### API

```bash
# Requer OAuth2 configurado
# Endpoint: https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
```

Orientar o usuário a acessar a interface web se a API não estiver configurada.

---

## 5. PageSpeed Insights / Core Web Vitals

API gratuita da Google, sem necessidade de autenticação.

### API

```bash
# Desktop
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&strategy=desktop&category=performance&category=seo&category=accessibility&category=best-practices"

# Mobile
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&strategy=mobile&category=performance&category=seo&category=accessibility&category=best-practices"
```

### Métricas Core Web Vitals

| Métrica | Bom | Precisa Melhorar | Ruim |
|---------|-----|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| FCP (First Contentful Paint) | < 1.8s | 1.8s - 3.0s | > 3.0s |
| TTFB (Time to First Byte) | < 800ms | 800ms - 1800ms | > 1800ms |

### Scores Lighthouse

| Categoria | Alvo |
|-----------|------|
| Performance | > 90 |
| Accessibility | > 90 |
| Best Practices | > 90 |
| SEO | > 90 |

### Script Disponível

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/marketing-analytics/scripts/pagespeed-report.sh https://aicodingflow.com
bash ${CLAUDE_PLUGIN_ROOT}/skills/marketing-analytics/scripts/pagespeed-report.sh https://aicodingflow.com desktop
bash ${CLAUDE_PLUGIN_ROOT}/skills/marketing-analytics/scripts/pagespeed-report.sh https://masterclaude.com
```

### Páginas Importantes para Testar

- `https://aicodingflow.com/` — Homepage
- `https://aicodingflow.com/curso` — Landing page do curso (CTA crítico)
- `https://aicodingflow.com/guide` — Claude Code Guide
- `https://masterclaude.com/` — Homepage masterclaude
- `https://masterclaude.com/articles` — Lista de artigos

---

## 6. Ferramentas SEO Externas

### Ahrefs

**Site:** https://ahrefs.com/
**Métricas:** Domain Rating (DR), backlinks, referring domains, organic keywords, organic traffic estimate

**Free tools (sem conta):**
- Backlink Checker: https://ahrefs.com/backlink-checker
- Website Authority Checker: https://ahrefs.com/website-authority-checker

**API (requer plano pago):**
```bash
curl -s "https://apiv2.ahrefs.com?from=domain_rating&target=aicodingflow.com&mode=domain&output=json&token=API_TOKEN"
```

### Moz

**Site:** https://moz.com/
**Métricas:** Domain Authority (DA), Page Authority (PA), Spam Score, linking domains

**Free tools:**
- Link Explorer: https://moz.com/link-explorer
- Domain Analysis: https://moz.com/domain-analysis

**API (requer plano):**
```bash
curl -s "https://lsapi.seomoz.com/v2/url_metrics" \
  -H "Authorization: Basic BASE64_ENCODED" \
  -d '{"targets": ["aicodingflow.com"]}'
```

### SEMrush

**Site:** https://www.semrush.com/
**Métricas:** Authority Score, organic traffic, paid traffic, backlinks, keyword rankings

**Free tools:**
- Domain Overview: https://www.semrush.com/analytics/overview/

**API (requer plano):**
```bash
curl -s "https://api.semrush.com/?type=domain_ranks&key=API_KEY&export_columns=Dn,Rk,Or,Ot,Oc,Ad,At&domain=aicodingflow.com"
```

### Alternativas Gratuitas para SEO

| Ferramenta | URL | Métricas |
|-----------|-----|----------|
| Ubersuggest | neilpatel.com/ubersuggest | Keywords, backlinks, traffic |
| SimilarWeb | similarweb.com | Traffic estimate, sources |
| Google Trends | trends.google.com | Search interest over time |
| AnswerThePublic | answerthepublic.com | Question-based keywords |

---

## 7. Google Ads

Conversion tracking configurado via `NEXT_PUBLIC_GOOGLE_ADS_ID`.

### Acesso

**Interface web:** https://ads.google.com/

### Métricas

- **Impressões**: quantas vezes o anúncio foi exibido
- **Cliques**: quantas vezes foi clicado
- **CTR**: click-through rate
- **CPC**: custo por clique
- **Conversões**: ações rastreadas (signup, purchase)
- **CPA**: custo por aquisição
- **ROAS**: retorno sobre investimento em ads

---

## Prioridade de Fontes por Pergunta

| Pergunta | Fonte Primária | Fonte Secundária |
|----------|---------------|-----------------|
| Quantos leads? | PostgreSQL | — |
| Quantas vendas? | PostgreSQL + Stripe | — |
| Receita total? | Stripe | PostgreSQL |
| Tráfego do site? | GA4 | SimilarWeb |
| Keywords orgânicas? | Search Console | SEMrush/Ahrefs |
| PageSpeed? | PageSpeed API | — |
| Domain authority? | Moz/Ahrefs | SEMrush |
| Backlinks? | Ahrefs | Moz |
| Checkouts abandonados? | PostgreSQL (leads) | Stripe (sessions) |
| Campanhas UTM? | PostgreSQL (leads) | GA4 |
| Email marketing? | PostgreSQL | — |
| Engajamento Guide? | PostgreSQL | GA4 |
