---
description: Marca Pull Request como pronto para revisão (remove status Draft)
argument-hint: [pr-number]
---

# PDIR: Ready PR

Marca Pull Request como pronto para revisão (remove status Draft).

## Entrada

`$ARGUMENTS` (opcional): Número do PR (ex: `123`)

Se não fornecido, marca PR da branch atual.

## Pré-Review (Opcional)

Antes de marcar como pronto, considere executar uma revisão automatizada com skills disponíveis:

- `/code-review` - Revisão de código do PR
- `/pr-review-toolkit:review-pr` - Revisão abrangente com agentes especializados
- Outras skills de revisão de código que você tenha instalado

## Instruções

```bash
gh pr ready $ARGUMENTS
```

### Feedback Final

```
PR marcado como pronto!

PR: #[número] - Ready for review

Próximo passo: /pdir-merge-tarefa
```

## Exemplo

```bash
/pdir-ready-pr        # PR da branch atual
/pdir-ready-pr 123    # PR específico
```
