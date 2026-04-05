#!/bin/bash
# Wrapper que instala dependencias automaticamente na primeira execucao
cd "$(dirname "$0")/.."
[ ! -d "node_modules" ] && npm install --production --silent 2>/dev/null
exec node server.js
