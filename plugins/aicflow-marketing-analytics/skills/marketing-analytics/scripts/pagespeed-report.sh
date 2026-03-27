#!/bin/bash
# Coleta e formata relatório de PageSpeed Insights + Core Web Vitals.
# Uso: bash pagespeed-report.sh <URL> [mobile|desktop]
# Exemplo: bash pagespeed-report.sh https://aicodingflow.com mobile

set -euo pipefail

URL="${1:?Uso: $0 <URL> [mobile|desktop]}"
STRATEGY="${2:-mobile}"

# Validar strategy
if [[ "$STRATEGY" != "mobile" && "$STRATEGY" != "desktop" ]]; then
  echo "Erro: strategy deve ser 'mobile' ou 'desktop'" >&2
  exit 1
fi

# Verificar jq
if ! command -v jq &>/dev/null; then
  echo "Erro: jq não instalado. Instale com: sudo apt install jq" >&2
  exit 1
fi

echo "=== PageSpeed Insights Report ==="
echo "URL: $URL"
echo "Strategy: $STRATEGY"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Chamar API
API_URL="https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${URL}&strategy=${STRATEGY}&category=performance&category=seo&category=accessibility&category=best-practices"

echo "Coletando dados..."
RESPONSE=$(curl -s "$API_URL")

# Verificar erro
if echo "$RESPONSE" | jq -e '.error' &>/dev/null; then
  echo "Erro da API:"
  echo "$RESPONSE" | jq -r '.error.message'
  exit 1
fi

echo ""

# Scores Lighthouse
echo "=== Lighthouse Scores ==="
echo "$RESPONSE" | jq -r '
  .lighthouseResult.categories | to_entries[] |
  "\(.value.title): \(.value.score * 100)%"
'

echo ""

# Core Web Vitals (dados de campo - CrUX)
echo "=== Core Web Vitals (Dados de Campo - CrUX) ==="
CRUX=$(echo "$RESPONSE" | jq '.loadingExperience.metrics // empty')

if [ -n "$CRUX" ] && [ "$CRUX" != "null" ]; then
  echo "$RESPONSE" | jq -r '
    .loadingExperience.metrics | to_entries[] |
    "\(.key): \(.value.percentile)\(.value.category // "")"
  '
  echo ""
  echo "Overall: $(echo "$RESPONSE" | jq -r '.loadingExperience.overall_category // "N/A"')"
else
  echo "Dados CrUX não disponíveis para esta URL (site pode ser muito novo ou ter pouco tráfego)."
fi

echo ""

# Métricas de Lab (Lighthouse)
echo "=== Métricas de Lab (Lighthouse) ==="
echo "$RESPONSE" | jq -r '
  .lighthouseResult.audits | {
    "First Contentful Paint": .["first-contentful-paint"].displayValue,
    "Largest Contentful Paint": .["largest-contentful-paint"].displayValue,
    "Total Blocking Time": .["total-blocking-time"].displayValue,
    "Cumulative Layout Shift": .["cumulative-layout-shift"].displayValue,
    "Speed Index": .["speed-index"].displayValue,
    "Time to Interactive": .["interactive"].displayValue
  } | to_entries[] | "\(.key): \(.value)"
'

echo ""

# Oportunidades de melhoria
echo "=== Oportunidades de Melhoria ==="
echo "$RESPONSE" | jq -r '
  [.lighthouseResult.audits | to_entries[] |
   select(.value.details.type? == "opportunity" and .value.score? != null and .value.score < 1)] |
  sort_by(.value.score)[:5][] |
  "- \(.value.title): \(.value.displayValue // "N/A") (score: \(.value.score * 100 | floor)%)"
'

echo ""

# Diagnósticos
echo "=== Diagnósticos ==="
echo "$RESPONSE" | jq -r '
  [.lighthouseResult.audits | to_entries[] |
   select(.value.details.type? == "table" and .value.score? != null and .value.score < 1)] |
  sort_by(.value.score)[:5][] |
  "- \(.value.title) (score: \(.value.score * 100 | floor)%)"
'

echo ""
echo "=== Fim do Relatório ==="
