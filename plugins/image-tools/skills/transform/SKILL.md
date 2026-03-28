---
name: transform
description: "Ferramentas de transformação e ajuste de imagens: redimensionar, rotacionar, espelhar, recortar, trim automático, padding, ajustes de brilho/contraste/saturação, escala de cinza, nitidez, desfoque, converter formatos e obter informações. Use esta skill sempre que o usuário pedir para redimensionar imagem, alterar dimensões, rotacionar (90°, 180°, 270° ou ângulo livre), espelhar/flipar, recortar região, aparar bordas (trim), adicionar margem/padding, ajustar brilho, contraste, saturação, converter para preto e branco/grayscale, aumentar nitidez (sharpen), desfocar (blur), converter formato (JPG↔PNG↔WebP etc.), criar thumbnail, ou ver informações de uma imagem. Também ativa para 'resize', 'rotate', 'flip', 'crop', 'trim', 'pad', 'brightness', 'contrast', 'sharpen', 'blur', 'grayscale', 'info', 'converter imagem', 'reduzir tamanho', 'trocar formato'. Inclui setup automático em virtualenv isolado."
---

# Image Transform

Ferramentas para transformar e ajustar imagens: redimensionar, rotacionar, espelhar, recortar, trim, padding, ajustes visuais, filtros e conversão de formatos.

Usa Pillow + numpy em virtualenv isolado em `~/venvs/image-transform/`.

## Setup

### Verificar se já está instalado

```bash
test -f ~/venvs/image-transform/bin/python && ~/venvs/image-transform/bin/python -c "import PIL; import numpy; print('OK')" || echo "PRECISA_INSTALAR"
```

### Instalar (se necessário)

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/setup.sh
```

## Uso

```bash
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py INPUT [OPÇÕES]
```

Transformações podem ser combinadas numa única execução. A ordem de aplicação é: trim → resize → crop → pad → rotate → flip → ajustes → filtros.

---

## Referência rápida

| Operação | Flag | Exemplo |
|----------|------|---------|
| Resize exato | `--resize WxH` | `--resize 800x600` |
| Escalar % | `--scale N` | `--scale 50` |
| Fit largura | `--fit-width N` | `--fit-width 1200` |
| Fit altura | `--fit-height N` | `--fit-height 800` |
| Rotacionar | `--rotate GRAUS` | `--rotate 90` |
| Espelhar | `--flip horizontal\|vertical` | `--flip horizontal` |
| Recortar | `--crop L,T,R,B` | `--crop 100,50,500,400` |
| Trim bordas | `--trim [--trim-fuzz N]` | `--trim --trim-fuzz 20` |
| Padding | `--pad N [--pad-color COR]` | `--pad 20 --pad-color "#f0f0f0"` |
| Brilho | `--brightness F` | `--brightness 1.3` |
| Contraste | `--contrast F` | `--contrast 1.2` |
| Saturação | `--saturation F` | `--saturation 0.5` |
| Escala cinza | `--grayscale` | `--grayscale` |
| Nitidez | `--sharpen` | `--sharpen` |
| Desfoque | `--blur R` | `--blur 2.0` |
| Formato | `--format EXT` | `--format webp` |
| Info | `--info` | `--info` |

---

## Redimensionar

| Opção | Descrição |
|-------|-----------|
| `--resize WxH` | Dimensões exatas (pode distorcer) |
| `--scale N` | Escalar por porcentagem (50 = 50%) |
| `--fit-width N` | Ajustar largura, manter proporção |
| `--fit-height N` | Ajustar altura, manter proporção |

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

Para ângulos que não são múltiplos de 90°, o canvas expande e o fundo é branco (RGB) ou transparente (RGBA/PNG).

---

## Espelhar (Flip)

```bash
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --flip horizontal
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --flip vertical
```

---

## Recortar

`--crop L,T,R,B` → esquerda, topo, direita, base (pixels, a partir do canto superior esquerdo).

```bash
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --crop 100,50,500,400
```

---

## Trim (aparar bordas)

`--trim` detecta a cor predominante nos cantos e remove bordas uniformes dessa cor.

`--trim-fuzz N` controla a tolerância (0-255, padrão: 10). Valores maiores removem mais variação de cor.

```bash
# Trim automático
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py screenshot.png --trim

# Trim com tolerância alta (remove bordas que não são exatamente uniformes)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --trim --trim-fuzz 30
```

---

## Padding

`--pad N` adiciona padding uniforme. `--pad T,R,B,L` para valores individuais (topo, direita, base, esquerda).

`--pad-color COR` aceita nomes (`white`, `black`, `red`, `green`, `blue`, `transparent`) ou hex (`#RRGGBB`).

```bash
# 20px branco ao redor
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py logo.png --pad 20

# Padding diferente em cada lado
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --pad 10,20,10,20

# Padding colorido
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --pad 30 --pad-color "#f0f0f0"
```

---

## Ajustes visuais

Todos os fatores usam 1.0 como valor original. Menor que 1.0 reduz, maior que 1.0 aumenta.

| Opção | Efeito |
|-------|--------|
| `--brightness F` | Brilho (0.0=preto, 1.0=original, 2.0=dobro) |
| `--contrast F` | Contraste (0.0=cinza uniforme, 1.0=original) |
| `--saturation F` | Saturação (0.0=cinza, 1.0=original, 2.0=super vibrante) |
| `--grayscale` | Converte para escala de cinza |

```bash
# Aumentar brilho e contraste
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --brightness 1.2 --contrast 1.1

# Converter para preto e branco
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --grayscale

# Reduzir saturação (efeito pastel)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --saturation 0.5
```

---

## Filtros

```bash
# Aumentar nitidez
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --sharpen

# Desfoque gaussiano (raio 3.0)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --blur 3.0
```

---

## Info

`--info` exibe informações da imagem em JSON (dimensões, formato, modo, tamanho, DPI) sem transformar.

```bash
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --info
```

---

## Converter formato

```bash
# JPG → PNG
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --format png

# PNG → WebP com qualidade 90
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py logo.png --format webp --quality 90
```

Formatos suportados: `jpg`, `png`, `webp`, `gif`, `bmp`, `tiff`

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

O original é renomeado para `_original` e a versão transformada salva no nome original.

### Com `--suffix` (preserva original intacto)

```bash
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --fit-width 200 --suffix _thumb
```

### Com `--output` (salva em outro local)

```bash
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --rotate 90 --output ~/Desktop/
```

---

## Combinações comuns

```bash
# Trim + resize + sharpen + WebP (pipeline completo para web)
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --trim --fit-width 1200 --sharpen --format webp

# Thumbnail com padding
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py foto.jpg --resize 200x200 --pad 10 --suffix _thumb

# Batch: ajustar + converter pasta inteira
~/venvs/image-transform/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/transform/scripts/transform.py ~/fotos/ --fit-width 1200 --brightness 1.1 --format webp --batch --suffix _web
```

---

## Fluxo de trabalho

1. Verificar se `~/venvs/image-transform/bin/python` existe
2. Se não existir, rodar o script de setup
3. Identificar arquivo(s) de entrada do usuário
4. Construir o comando com as transformações solicitadas
5. Executar o script
6. Confirmar resultado (dimensões, tamanho do arquivo) ao usuário
