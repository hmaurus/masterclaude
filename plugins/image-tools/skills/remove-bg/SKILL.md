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

Executar o script de setup:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/remove-bg/scripts/setup.sh
```

Na primeira execução do rembg, o modelo U²-Net (~170MB) é baixado automaticamente para `~/.u2net/`. Avisar o usuário sobre esse download.

## Uso

### Imagem única

```bash
~/venvs/rembg/bin/rembg i <entrada> <saida>
```

### Pasta inteira (batch)

```bash
~/venvs/rembg/bin/rembg p <pasta-entrada>/ <pasta-saida>/
```

### Exemplos

```bash
# PNG → PNG
~/venvs/rembg/bin/rembg i foto.png foto-sem-fundo.png

# JPG → PNG com transparência
~/venvs/rembg/bin/rembg i foto.jpg foto-sem-fundo.png

# Batch: todas as imagens de uma pasta
~/venvs/rembg/bin/rembg p originais/ sem-fundo/

# Com modelo específico para pessoas
~/venvs/rembg/bin/rembg i -m u2net_human_seg retrato.jpg retrato-sem-fundo.png

# Com alpha matting (bordas mais suaves)
~/venvs/rembg/bin/rembg i -a -ae 10 -ab 10 foto.png foto-suave.png
```

## Opções úteis

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

Trocar modelo: adicionar `-m <nome>` ao comando.

## Fluxo de trabalho

1. Verificar se `~/venvs/rembg/bin/rembg` existe
2. Se não existir, rodar o script de setup
3. Identificar arquivo(s) de entrada do usuário
4. Escolher modelo adequado (pessoas → `u2net_human_seg`, geral → `u2net`)
5. Executar rembg
6. Confirmar resultado ao usuário

## Notas

- Saída sempre em PNG para suportar transparência
- Se a entrada for JPG/JPEG, a saída deve ser `.png`
- Sugerir `u2net_human_seg` quando a imagem contém pessoas
- Para bordas mais suaves (cabelo, pelos), sugerir alpha matting (`-a`)
