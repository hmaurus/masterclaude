---
name: remove-watermark
description: "Remove marcas d'água de imagens, especialmente de geradores de IA como Google Gemini, Nano Banana, DALL-E, Midjourney etc. Use esta skill quando o usuário pedir para remover watermark, marca d'água, logo de IA, selo de gerador, ou limpar imagem gerada por IA. Também ativa quando o usuário menciona 'marca d'água', 'watermark', 'logo do gemini', 'selo da IA' ou quer limpar cantos de imagens de IA. Inclui setup automático em virtualenv isolado com OpenCV."
---

# Remove Marca d'Água de Imagens

Remove marcas d'água de imagens usando OpenCV inpainting. Especializado em marcas de geradores de IA (Google Gemini, Nano Banana, DALL-E, etc.) que ficam tipicamente nos cantos da imagem.

O inpainting preenche a região da marca d'água com o conteúdo visual ao redor, reconstruindo a imagem de forma natural — diferente de simplesmente recortar.

## Setup

O ambiente fica em `~/venvs/watermark-remover/` isolado do sistema.

### Verificar se já está instalado

```bash
test -d ~/venvs/watermark-remover && ~/venvs/watermark-remover/bin/python -c "import cv2; print('OK')" || echo "PRECISA_INSTALAR"
```

### Instalar (se necessário)

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/setup.sh
```

## Uso

O script fica em `${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py`.

### Imagem única (marca d'água no canto inferior direito — padrão)

```bash
~/venvs/watermark-remover/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py entrada.png saida.png
```

### Especificar canto

```bash
# Canto inferior esquerdo
~/venvs/watermark-remover/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py entrada.png saida.png -c bl

# Canto superior direito
~/venvs/watermark-remover/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py entrada.png saida.png -c tr
```

### Ajustar tamanho da região

```bash
# Marca d'água maior (12% da imagem em vez do padrão 8%)
~/venvs/watermark-remover/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py entrada.png saida.png -s 12

# Marca d'água bem pequena (5%)
~/venvs/watermark-remover/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py entrada.png saida.png -s 5
```

### Região manual (coordenadas em pixels)

Quando a marca d'água não está no canto ou tem posição irregular:

```bash
# --rect x1,y1,x2,y2 (canto superior esquerdo e inferior direito da região)
~/venvs/watermark-remover/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py entrada.png saida.png --rect 700,450,800,500
```

### Batch (pasta inteira)

```bash
~/venvs/watermark-remover/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-watermark/scripts/remove_watermark.py pasta_entrada/ pasta_saida/
```

## Opções

| Flag | Padrão | Descrição |
|------|--------|-----------|
| `-c, --corner` | `br` | Canto: `br` (inferior-direito), `bl`, `tr`, `tl` |
| `-s, --size` | `8` | Tamanho da região (% da imagem) |
| `-p, --padding` | `10` | Padding extra em pixels ao redor da região |
| `-r, --radius` | `5` | Raio do inpainting (maior = mais suave, mas mais lento) |
| `-f, --feather` | `15` | Suavização das bordas da máscara |
| `--rect` | — | Região manual: `x1,y1,x2,y2` em pixels |

## Marcas d'água comuns por gerador

| Gerador | Posição | Tamanho sugerido |
|---------|---------|------------------|
| Google Gemini | inferior-direito | 5-8% (`-c br -s 6`) |
| Nano Banana | inferior-direito | 8-10% (`-c br -s 9`) |
| DALL-E | inferior-direito | 5% (`-c br -s 5`) |

## Fluxo de trabalho

1. Verificar se `~/venvs/watermark-remover/` existe
2. Se não, rodar o script de setup
3. Identificar a imagem e a posição da marca d'água (perguntar ao usuário se não for óbvio)
4. Escolher parâmetros adequados baseado no gerador (ver tabela acima)
5. Executar o script
6. Mostrar/confirmar resultado ao usuário

## Dicas para melhores resultados

- Se o resultado ficou com artefatos visíveis, aumentar o raio (`-r 8` ou `-r 10`)
- Para marcas d'água muito pequenas (ícones), reduzir o tamanho (`-s 4 -s 5`)
- Para marcas d'água maiores (texto longo), aumentar o tamanho (`-s 12 -s 15`)
- Se a borda do preenchimento ficou visível, aumentar o feather (`-f 20`)
- Para marcas d'água fora dos cantos, usar `--rect` com coordenadas exatas
- O resultado funciona melhor quando o fundo ao redor da marca d'água é relativamente uniforme (gradientes, cores sólidas)
