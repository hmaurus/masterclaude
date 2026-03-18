---
name: transform
description: "Ferramentas de transformação de imagens: redimensionar, rotacionar de várias formas, espelhar, recortar e converter formatos. Use esta skill sempre que o usuário pedir para redimensionar imagem, alterar dimensões, rotacionar (90°, 180°, 270° ou ângulo livre), espelhar/flipar horizontalmente ou verticalmente, recortar região, converter formato (JPG para PNG, PNG para WebP, etc.), criar thumbnail, ou mencionar 'resize', 'rotate', 'flip', 'crop', 'converter imagem', 'reduzir tamanho', 'trocar formato'. Também ativa quando o usuário quer alterar dimensões, ângulo, orientação ou formato de uma ou várias imagens. Inclui setup automático em virtualenv isolado."
---

# Image Transform

Ferramentas para transformar imagens: redimensionar, rotacionar, espelhar, recortar e converter formatos.

Usa Pillow (PIL) instalado em virtualenv isolado em `~/venvs/image-transform/`.

## Setup

O Pillow fica em `~/venvs/image-transform/` para não poluir o sistema. Na primeira vez, o setup precisa ser executado.

### Verificar se já está instalado

```bash
test -f ~/venvs/image-transform/bin/python && ~/venvs/image-transform/bin/python -c "import PIL; print('OK')" || echo "PRECISA_INSTALAR"
```

### Instalar (se necessário)

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/setup.sh
```

## Uso

O script fica em `${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py`.

### Sintaxe geral

```bash
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py INPUT [OPÇÕES]
```

Transformações podem ser combinadas numa única execução.

---

## Redimensionar

| Opção | Descrição | Exemplo |
|-------|-----------|---------|
| `--resize WxH` | Dimensões exatas (pode distorcer) | `--resize 800x600` |
| `--scale N` | Escalar por porcentagem | `--scale 50` (= 50%) |
| `--fit-width N` | Ajustar largura, manter proporção | `--fit-width 1200` |
| `--fit-height N` | Ajustar altura, manter proporção | `--fit-height 800` |

```bash
# Redimensionar para 800x600 exatos
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --resize 800x600

# Reduzir 50%
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --scale 50

# Ajustar largura para 1200px, manter proporção
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --fit-width 1200
```

---

## Rotacionar

`--rotate N` rotaciona **N graus no sentido anti-horário**.

- `--rotate 90` → 90° anti-horário (vira para esquerda)
- `--rotate -90` ou `--rotate 270` → 90° horário (vira para direita)
- `--rotate 180` → de cabeça para baixo
- `--rotate 45` → diagonal (ângulo livre, canvas expande)

```bash
# 90 graus anti-horário
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 90

# 90 graus horário
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 270

# 180 graus
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 180

# Ângulo livre com fundo branco
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 45
```

Para ângulos que não são múltiplos de 90°, o canvas expande para acomodar toda a imagem e o fundo é preenchido com branco (RGB) ou transparente (RGBA/PNG).

---

## Espelhar (Flip)

```bash
# Espelho horizontal (como selfie invertida)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --flip horizontal

# Espelho vertical (de cabeça para baixo)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --flip vertical
```

---

## Recortar

`--crop L,T,R,B` → esquerda, topo, direita, base (em pixels, a partir do canto superior esquerdo).

```bash
# Recortar região de (100,50) até (500,400)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --crop 100,50,500,400
```

---

## Converter formato

```bash
# JPG → PNG
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --format png

# PNG → WebP com qualidade 90
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py logo.png --format webp --quality 90

# JPG → WebP (reduz tamanho)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --format webp
```

Formatos suportados na saída: `jpg`, `png`, `webp`, `gif`, `bmp`, `tiff`

---

## Opções de saída

| Opção | Descrição |
|-------|-----------|
| `--quality N` | Qualidade JPG/WebP (1–95, padrão: 85) |
| `--output CAMINHO` | Arquivo ou diretório de saída |
| `--suffix TEXTO` | Sufixo no nome (ex: `_thumb`) — preserva original |
| `--no-backup` | Sobrescreve o original sem fazer backup |
| `--batch` | Processa todos os arquivos de um diretório |

### Comportamento padrão (sem `--output` ou `--suffix`)

O original é renomeado para `_original` e a versão transformada salva no nome original:

```bash
# foto.jpg → foto_original.jpg (backup) + foto.jpg (transformada)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 90
```

### Com `--suffix` (preserva original intacto)

```bash
# foto.jpg (intacta) + foto_thumb.jpg (nova)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --fit-width 200 --suffix _thumb
```

### Com `--output` (salva em outro local)

```bash
# foto.jpg (intacta), salva em ~/Desktop/foto.jpg
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 90 --output ~/Desktop/
```

---

## Combinações comuns

```bash
# Redimensionar + converter para WebP
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --fit-width 1200 --format webp --quality 85

# Rotacionar + salvar em pasta específica
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 90 --output ~/Desktop/

# Thumbnail 200x200 sem alterar original
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --resize 200x200 --suffix _thumb

# Batch: ajustar largura de todas as imagens de uma pasta
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py ~/fotos/ --fit-width 1200 --batch --suffix _web

# Recortar + rotacionar
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --crop 0,100,800,700 --rotate 90
```

---

## Fluxo de trabalho

1. Verificar se `~/venvs/image-transform/bin/python` existe
2. Se não existir, rodar o script de setup
3. Identificar arquivo(s) de entrada do usuário
4. Construir o comando com as transformações solicitadas
5. Executar o script
6. Confirmar resultado (dimensões, tamanho do arquivo) ao usuário
