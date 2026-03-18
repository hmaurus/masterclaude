#!/usr/bin/env bash
# Setup do ambiente para remoção de marca d'água (~/.venvs/watermark-remover)
# Dependências: opencv-python-headless, numpy
# Uso: bash setup.sh

set -euo pipefail

VENV_DIR="$HOME/venvs/watermark-remover"

if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/python" ]; then
  echo "Ambiente já instalado em $VENV_DIR"
  "$VENV_DIR/bin/python" -c "import cv2; print(f'OpenCV {cv2.__version__}')"
  exit 0
fi

echo "Criando virtualenv em $VENV_DIR..."
python3 -m venv "$VENV_DIR"

echo "Instalando dependências..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install opencv-python-headless numpy

echo ""
echo "Instalação concluída!"
"$VENV_DIR/bin/python" -c "import cv2; print(f'OpenCV {cv2.__version__}')"
