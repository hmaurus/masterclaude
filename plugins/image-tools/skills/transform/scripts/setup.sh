#!/bin/bash
# Setup script para image-transform (Pillow em virtualenv isolado)

VENV_DIR="$HOME/venvs/image-transform"

echo "Configurando virtualenv em $VENV_DIR..."

if [ -d "$VENV_DIR" ]; then
    echo "Virtualenv já existe. Verificando instalação..."
else
    python3 -m venv "$VENV_DIR"
    echo "Virtualenv criado."
fi

echo "Instalando/atualizando Pillow..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet "Pillow>=10.0.0"

echo ""
echo "✓ Pillow instalado com sucesso!"
"$VENV_DIR/bin/python" -c "from PIL import Image; print('  Versão:', Image.__version__ if hasattr(Image, '__version__') else 'OK')"
echo ""
echo "Uso: $VENV_DIR/bin/python transform.py --help"
