# KPIs e Benchmarks — Marketing SaaS / Infoproduto

Definições de KPIs e benchmarks de mercado para contextualizar métricas do aicodingflow.com.

---

## KPIs de Leads & Conversão

### Definições

| KPI | Fórmula | Descrição |
|-----|---------|-----------|
| **Total de Leads** | COUNT(leads) | Número absoluto de leads capturados |
| **Leads por Dia** | leads / dias | Média diária de novos leads |
| **Taxa de Conversão** | (convertidos / total_leads) × 100 | % de leads que viraram compra |
| **Leads por Fonte** | GROUP BY source | Distribuição checkout vs newsletter vs popup |
| **Custo por Lead (CPL)** | gasto_ads / total_leads | Custo para adquirir cada lead |
| **Taxa de Abandono** | leads_checkout_nao_convertidos / leads_checkout | % que iniciou checkout mas não comprou |

### Benchmarks (SaaS / Infoproduto)

| Métrica | Fraco | Médio | Bom | Excelente |
|---------|-------|-------|-----|-----------|
| Taxa de conversão (lead → venda) | < 1% | 1-3% | 3-5% | > 5% |
| Taxa de conversão landing page | < 2% | 2-5% | 5-10% | > 10% |
| Taxa de abandono de checkout | > 80% | 70-80% | 60-70% | < 60% |
| Email opt-in rate | < 1% | 1-3% | 3-5% | > 5% |

---

## KPIs de Receita

### Definições

| KPI | Fórmula | Descrição |
|-----|---------|-----------|
| **Receita Bruta** | SUM(amount_paid) | Total faturado (em centavos → dividir por 100) |
| **Receita Líquida** | receita_bruta - fees_stripe | Após taxas de processamento |
| **Ticket Médio** | receita / vendas | Valor médio por transação |
| **Receita por Produto** | GROUP BY product | Guide vs Curso |
| **Receita por Moeda** | GROUP BY currency | BRL vs USD |
| **Receita Mensal** | GROUP BY month | Tendência de crescimento |
| **LTV (Lifetime Value)** | receita_total / clientes_unicos | Valor total por cliente |
| **ARPU** | receita_mensal / usuarios_ativos | Receita média por usuário |

### Taxas Stripe

- Cartão nacional (Brasil): 3.99% + R$ 0,39
- Cartão internacional: 5.99% + R$ 0,39
- PIX: 0.99%

### Benchmarks

| Métrica | Contexto |
|---------|----------|
| Ticket médio curso online | R$ 197 - R$ 997 (Brasil) |
| Ticket médio SaaS individual | $10 - $50/mês |
| LTV:CAC ratio ideal | > 3:1 |
| Payback period | < 12 meses |

---

## KPIs de SEO & Busca

### Definições

| KPI | Fonte | Descrição |
|-----|-------|-----------|
| **Impressões** | Search Console | Vezes que o site apareceu no Google |
| **Cliques orgânicos** | Search Console | Vezes que foi clicado na busca |
| **CTR orgânico** | Search Console | cliques / impressões |
| **Posição média** | Search Console | Posição média nos resultados |
| **Domain Rating (DR)** | Ahrefs | Score de autoridade (0-100) |
| **Domain Authority (DA)** | Moz | Score de autoridade (0-100) |
| **Authority Score** | SEMrush | Score de autoridade (0-100) |
| **Backlinks** | Ahrefs/Moz | Total de links apontando para o site |
| **Referring Domains** | Ahrefs/Moz | Domínios únicos com backlinks |
| **Organic Keywords** | SEMrush/Ahrefs | Keywords para as quais o site ranqueia |
| **Organic Traffic** | SEMrush/Ahrefs | Estimativa de tráfego orgânico mensal |

### Benchmarks (Sites novos < 1 ano)

| Métrica | Fraco | Médio | Bom | Excelente |
|---------|-------|-------|-----|-----------|
| Domain Authority (DA) | < 10 | 10-20 | 20-30 | > 30 |
| Domain Rating (DR) | < 10 | 10-20 | 20-30 | > 30 |
| Organic keywords | < 50 | 50-200 | 200-1000 | > 1000 |
| Backlinks | < 20 | 20-100 | 100-500 | > 500 |
| Referring domains | < 10 | 10-30 | 30-100 | > 100 |
| CTR orgânico (posição 1) | — | — | 25-35% | > 35% |
| CTR orgânico (posição 2-3) | — | — | 10-20% | > 20% |
| CTR orgânico (posição 4-10) | — | — | 3-10% | > 10% |

---

## KPIs de Performance Técnica

### Core Web Vitals

| Métrica | Bom | Precisa Melhorar | Ruim |
|---------|-----|-------------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **FCP** (First Contentful Paint) | < 1.8s | 1.8s - 3.0s | > 3.0s |
| **TTFB** (Time to First Byte) | < 800ms | 800ms - 1800ms | > 1800ms |

### Lighthouse Scores

| Categoria | Alvo | Impacto |
|-----------|------|---------|
| **Performance** | > 90 | Velocidade e UX — impacta SEO e conversão |
| **Accessibility** | > 90 | Conformidade WCAG — impacta SEO |
| **Best Practices** | > 90 | Segurança e padrões web |
| **SEO** | > 90 | Otimização técnica para buscadores |

### Impacto da Performance na Conversão

Dados da indústria (Google, Portent):
- Cada 1s adicional no carregamento reduz conversão em ~7%
- Sites com LCP < 2.5s têm 24% mais conversão que sites com LCP > 4.0s
- Mobile: 53% dos usuários abandonam se carregamento > 3s
- CLS ruim aumenta bounce rate em até 15%

---

## KPIs de Tráfego

### Definições

| KPI | Fonte | Descrição |
|-----|-------|-----------|
| **Sessões** | GA4 | Total de visitas |
| **Usuários** | GA4 | Visitantes únicos |
| **Novos vs Recorrentes** | GA4 | Proporção de novos visitantes |
| **Pageviews** | GA4 | Total de páginas visualizadas |
| **Pages/Session** | GA4 | Média de páginas por visita |
| **Bounce Rate** | GA4 | % que saiu sem interagir |
| **Duração Média** | GA4 | Tempo médio na sessão |
| **Fontes de Tráfego** | GA4 | Organic, Direct, Social, Referral, Paid |

### Benchmarks (Blog/SaaS)

| Métrica | Fraco | Médio | Bom | Excelente |
|---------|-------|-------|-----|-----------|
| Bounce rate (blog) | > 80% | 60-80% | 40-60% | < 40% |
| Bounce rate (landing) | > 70% | 50-70% | 30-50% | < 30% |
| Pages/session | < 1.5 | 1.5-2.5 | 2.5-4.0 | > 4.0 |
| Session duration | < 30s | 30s-2min | 2-5min | > 5min |
| New vs returning | > 90% new | 70-90% new | 50-70% new | Equilíbrio |

---

## KPIs de Email Marketing

### Definições

| KPI | Fórmula | Descrição |
|-----|---------|-----------|
| **Enrollments Ativos** | COUNT WHERE status='active' | Contatos em sequências ativas |
| **Taxa de Conclusão** | completed / total | % que completou a sequência |
| **Taxa de Cancelamento** | cancelled / total | % que saiu da sequência |
| **Step Médio** | AVG(current_step) | Progresso médio na sequência |

### Benchmarks (Email Sequences)

| Métrica | Fraco | Médio | Bom | Excelente |
|---------|-------|-------|-----|-----------|
| Open rate | < 15% | 15-25% | 25-35% | > 35% |
| Click rate | < 1% | 1-3% | 3-5% | > 5% |
| Unsubscribe rate | > 1% | 0.5-1% | 0.2-0.5% | < 0.2% |
| Sequence completion | < 30% | 30-50% | 50-70% | > 70% |

---

## KPIs de Ads (Google Ads)

### Definições

| KPI | Fórmula | Descrição |
|-----|---------|-----------|
| **Impressões** | — | Exibições do anúncio |
| **Cliques** | — | Cliques no anúncio |
| **CTR** | cliques / impressões | Taxa de clique |
| **CPC** | gasto / cliques | Custo por clique |
| **CPA** | gasto / conversões | Custo por aquisição |
| **ROAS** | receita / gasto_ads | Retorno sobre investimento |
| **Conversion Rate** | conversões / cliques | Taxa de conversão pós-clique |

### Benchmarks (Educação / SaaS)

| Métrica | Fraco | Médio | Bom | Excelente |
|---------|-------|-------|-----|-----------|
| CTR (Search) | < 2% | 2-4% | 4-6% | > 6% |
| CTR (Display) | < 0.1% | 0.1-0.5% | 0.5-1% | > 1% |
| CPC (Brasil, educação) | > R$ 5 | R$ 2-5 | R$ 1-2 | < R$ 1 |
| CPA (infoproduto) | > R$ 200 | R$ 100-200 | R$ 50-100 | < R$ 50 |
| ROAS | < 2x | 2-4x | 4-8x | > 8x |

---

## Framework de Análise

### Funil Completo do AICFlow

```
Visitante (GA4)
  → Lead capturado (DB: leads table)
    → Email nurture (DB: email_enrollments)
      → Checkout iniciado (DB: leads WHERE source='checkout')
        → Compra (DB: purchases + Stripe)
          → Recompra / Upsell (Guide → Curso)
```

### Métricas por Estágio

| Estágio | Métrica Principal | Meta |
|---------|-------------------|------|
| Awareness | Impressões (GSC), Tráfego (GA4) | Crescimento MoM > 10% |
| Interest | Pageviews, Tempo no site | Bounce < 60%, Duration > 2min |
| Consideration | Leads capturados | Conversão visitante→lead > 3% |
| Intent | Checkouts iniciados | Conversão lead→checkout > 20% |
| Purchase | Vendas | Conversão checkout→compra > 40% |
| Retention | Guide progress, Recompra | Completion > 30%, Upsell > 5% |

### Comparações Úteis

Sempre apresentar dados com contexto temporal:
- **WoW** (Week over Week): comparar com semana anterior
- **MoM** (Month over Month): comparar com mês anterior
- **YoY** (Year over Year): comparar com mesmo período do ano anterior
- **Acumulado**: total desde o lançamento

### Red Flags (Alertas)

Situações que merecem atenção imediata:
- Taxa de conversão caiu > 20% WoW
- Bounce rate subiu > 10 pontos percentuais
- PageSpeed score caiu abaixo de 80
- Checkouts abandonados > 80%
- Zero leads em um dia útil
- Queda de impressões orgânicas > 30% MoM
