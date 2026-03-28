#!/bin/bash
# Setup script para image-transform (Pillow + numpy em virtualenv isolado)

VENV_DIR="$HOME/venvs/image-transform"

echo "Configurando virtualenv em $VENV_DIR..."

if [ -d "$VENV_DIR" ]; then
    echo "Virtualenv já existe. Verificando instalação..."
else
    python3 -m venv "$VENV_DIR"
    echo "Virtualenv criado."
fi

echo "Instalando/atualizando dependências..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet "Pillow>=10.0.0" "numpy>=1.24.0"

echo ""
echo "✓ Dependências instaladas com sucesso!"
"$VENV_DIR/bin/python" -c "from PIL import Image; import numpy; print('  Pillow:', Image.__version__ if hasattr(Image, '__version__') else 'OK'); print('  numpy:', numpy.__version__)"
echo ""
echo "Uso: $VENV_DIR/bin/python transform.py --help"
