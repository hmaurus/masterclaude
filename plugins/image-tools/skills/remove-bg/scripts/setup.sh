#!/usr/bin/env bash
# Setup do rembg em virtualenv isolado (~/.venvs/rembg)
# Uso: bash setup.sh

set -euo pipefail

VENV_DIR="$HOME/venvs/rembg"

if [ -f "$VENV_DIR/bin/rembg" ]; then
  echo "rembg já instalado em $VENV_DIR"
  "$VENV_DIR/bin/rembg" --version
  exit 0
fi

echo "Criando virtualenv em $VENV_DIR..."
python3 -m venv "$VENV_DIR"

echo "Instalando rembg[cli]..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install "rembg[cli]"

echo ""
echo "Instalação concluída!"
"$VENV_DIR/bin/rembg" --version
echo ""
echo "Na primeira execução, o modelo U²-Net (~170MB) será baixado automaticamente."
