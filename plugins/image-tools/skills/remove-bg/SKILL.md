---
name: remove-bg
description: "Remove background de imagens usando rembg (IA). Use esta skill sempre que o usuário pedir para remover fundo/background de imagem, recortar sujeito, criar PNG com transparência, isolar sujeito do fundo, ou mencionar 'rembg'. Também ativa quando o usuário referencia uma imagem e quer extrair o sujeito ou tornar o fundo transparente. Inclui setup automático em virtualenv isolado."
---

# Remove Background de Imagem

Remove o fundo de imagens usando `rembg` (modelo U²-Net), instalado em virtualenv isolado em `~/venvs/rembg/`.

## Setup

O rembg fica em `~/venvs/rembg/` para não poluir o sistema. Na primeira vez, o setup precisa ser executado.

### Verificar se já está instalado

```bash
test -f ~/venvs/rembg/bin/rembg && ~/venvs/rembg/bin/rembg --version || echo "PRECISA_INSTALAR"
```

### Instalar (se necessário)

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/setup.sh
```

Na primeira execução do rembg, o modelo U²-Net (~170MB) é baixado automaticamente para `~/.u2net/`. Avisar o usuário sobre esse download.

## Uso

O script wrapper fica em `${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/remove_bg.py`.

### Imagem única (saída automática — padrão)

Sem argumento de saída, renomeia a original para `_original` e salva a imagem sem fundo com o nome original:

```bash
# foto.png → foto_original.png (com fundo) + foto.png (sem fundo)
~/venvs/rembg/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/remove_bg.py foto.png
```

### Com saída explícita

```bash
~/venvs/rembg/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/remove_bg.py entrada.png saida.png
```

### Com modelo para pessoas

```bash
~/venvs/rembg/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/remove_bg.py retrato.jpg -m u2net_human_seg
```

### Com alpha matting (bordas mais suaves)

```bash
~/venvs/rembg/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/remove_bg.py foto.png -a -ae 10 -ab 10
```

### Batch (pasta inteira)

```bash
# Com pasta de saída separada
~/venvs/rembg/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/remove_bg.py pasta_entrada/ pasta_saida/

# In-place (renomeia originais para _original, salva limpas no nome original)
~/venvs/rembg/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/remove_bg.py pasta/
```

## Opções

| Flag | Descrição |
|------|-----------|
| `-m <modelo>` | Escolher modelo (ver tabela abaixo) |
| `-a` | Ativar alpha matting (bordas mais suaves) |
| `-ae <N>` | Erosão do alpha matting (padrão: 10) |
| `-ab <N>` | Blur do alpha matting (padrão: 10) |

## Modelos disponíveis

| Modelo | Melhor para |
|--------|-------------|
| `u2net` (padrão) | Uso geral |
| `u2net_human_seg` | Pessoas e retratos |
| `isnet-general-use` | Objetos variados |
| `silueta` | Leve e rápido |

## Fluxo de trabalho

1. Verificar se `~/venvs/rembg/bin/rembg` existe
2. Se não existir, rodar o script de setup
3. Identificar arquivo(s) de entrada do usuário
4. Escolher modelo adequado (pessoas → `u2net_human_seg`, geral → `u2net`)
5. Executar o script wrapper
6. Confirmar resultado ao usuário

## Notas

- Saída sempre em PNG para suportar transparência
- Se a entrada for JPG/JPEG, a saída será `.png`
- Sugerir `u2net_human_seg` quando a imagem contém pessoas
- Para bordas mais suaves (cabelo, pelos), sugerir alpha matting (`-a`)
