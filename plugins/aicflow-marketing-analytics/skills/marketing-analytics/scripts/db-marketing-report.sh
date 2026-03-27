#!/bin/bash
# Gera relatório de marketing a partir do banco de dados PostgreSQL.
# Uso: bash db-marketing-report.sh [production|local]
# Default: local (usa DATABASE_URL do .env)
# Production: conecta via SSH na VPS

set -euo pipefail

ENV="${1:-local}"
PROJECT_DIR="${AICFLOW_PROJECT_DIR:-/home/mh/dev/aicodingflow}"

run_query() {
  local query="$1"
  if [ "$ENV" = "production" ]; then
    ssh mh-vps "docker exec -i aicodingflow-db psql -U aicodingflow -d aicodingflow -t -A -F'|'" <<< "$query"
  else
    # Ler DATABASE_URL do .env
    local db_url
    db_url=$(grep -E '^DATABASE_URL=' "$PROJECT_DIR/.env" 2>/dev/null | cut -d'=' -f2- | tr -d '"')
    if [ -z "$db_url" ]; then
      echo "Erro: DATABASE_URL não encontrada em $PROJECT_DIR/.env" >&2
      exit 1
    fi
    psql "$db_url" -t -A -F'|' -c "$query"
  fi
}

echo "========================================"
echo "  RELATÓRIO DE MARKETING — AICFlow"
echo "  Ambiente: $ENV"
echo "  Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Dashboard rápido
echo "=== DASHBOARD GERAL ==="
run_query "
SELECT
  (SELECT COUNT(*) FROM leads) as total_leads,
  (SELECT COUNT(*) FROM leads WHERE converted = true) as leads_convertidos,
  (SELECT COUNT(*) FROM purchases WHERE status = 'completed') as total_compras,
  (SELECT COUNT(*) FROM users) as total_usuarios,
  (SELECT COUNT(*) FROM email_enrollments WHERE status = 'active') as emails_ativos;
"
echo ""

# Leads por produto e fonte
echo "=== LEADS POR PRODUTO E FONTE ==="
run_query "
SELECT
  product,
  source,
  COUNT(*) as total,
  SUM(CASE WHEN converted THEN 1 ELSE 0 END) as convertidos,
  ROUND(100.0 * SUM(CASE WHEN converted THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) as taxa_conversao
FROM leads
GROUP BY product, source
ORDER BY total DESC;
"
echo ""

# Receita por produto e moeda
echo "=== RECEITA POR PRODUTO ==="
run_query "
SELECT
  product,
  plan,
  currency,
  COUNT(*) as vendas,
  SUM(amount_paid) / 100.0 as receita,
  ROUND(AVG(amount_paid) / 100.0, 2) as ticket_medio
FROM purchases
WHERE status = 'completed'
GROUP BY product, plan, currency
ORDER BY receita DESC;
"
echo ""

# Leads últimos 30 dias
echo "=== LEADS ÚLTIMOS 30 DIAS (por dia) ==="
run_query "
SELECT
  TO_CHAR(created_at, 'YYYY-MM-DD') as dia,
  product,
  COUNT(*) as novos
FROM leads
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY dia, product
ORDER BY dia DESC;
"
echo ""

# Compras últimos 30 dias
echo "=== COMPRAS ÚLTIMOS 30 DIAS ==="
run_query "
SELECT
  TO_CHAR(created_at, 'YYYY-MM-DD') as dia,
  product,
  plan,
  currency,
  COUNT(*) as vendas,
  SUM(amount_paid) / 100.0 as receita
FROM purchases
WHERE status = 'completed' AND created_at >= NOW() - INTERVAL '30 days'
GROUP BY dia, product, plan, currency
ORDER BY dia DESC;
"
echo ""

# Top UTM Campaigns
echo "=== TOP CAMPANHAS UTM ==="
run_query "
SELECT
  COALESCE(utm_source, '-') as source,
  COALESCE(utm_medium, '-') as medium,
  COALESCE(utm_campaign, '-') as campaign,
  COUNT(*) as leads,
  SUM(CASE WHEN converted THEN 1 ELSE 0 END) as convertidos
FROM leads
WHERE utm_source IS NOT NULL
GROUP BY utm_source, utm_medium, utm_campaign
ORDER BY leads DESC
LIMIT 15;
"
echo ""

# Checkouts abandonados
echo "=== CHECKOUTS ABANDONADOS ==="
run_query "
SELECT
  product,
  COUNT(*) as abandonados,
  (SELECT COUNT(*) FROM purchases p WHERE p.product = l.product AND p.status = 'completed') as compras,
  ROUND(
    100.0 * COUNT(*) / NULLIF(
      COUNT(*) + (SELECT COUNT(*) FROM purchases p WHERE p.product = l.product AND p.status = 'completed'), 0
    ), 1
  ) as taxa_abandono
FROM leads l
WHERE source = 'checkout' AND converted = false
GROUP BY product;
"
echo ""

# Email Marketing
echo "=== EMAIL MARKETING ==="
run_query "
SELECT
  s.name as sequencia,
  e.status,
  COUNT(*) as total,
  ROUND(AVG(e.current_step), 1) as step_medio
FROM email_enrollments e
LEFT JOIN email_sequences s ON e.sequence_id = s.id
GROUP BY s.name, e.status
ORDER BY s.name, e.status;
"
echo ""

# Novos usuários por semana
echo "=== NOVOS USUÁRIOS POR SEMANA (últimas 8 semanas) ==="
run_query "
SELECT
  DATE_TRUNC('week', created_at)::date as semana,
  COUNT(*) as novos_usuarios
FROM users
WHERE created_at >= NOW() - INTERVAL '8 weeks'
GROUP BY semana
ORDER BY semana DESC;
"
echo ""

# Progresso Guide (engajamento)
echo "=== ENGAJAMENTO NO GUIDE (seções mais completadas) ==="
run_query "
SELECT
  section_slug,
  COUNT(DISTINCT user_id) as usuarios
FROM guide_progress
GROUP BY section_slug
ORDER BY usuarios DESC
LIMIT 10;
"
echo ""

echo "========================================"
echo "  FIM DO RELATÓRIO"
echo "========================================"
