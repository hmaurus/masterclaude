---
description: Marca Pull Request como pronto para revisão (remove status Draft)
argument-hint: [pr-number]
---

# PDIR: Ready PR

Marca Pull Request como pronto para revisão (remove status Draft).

## Entrada

`$ARGUMENTS` (opcional): Número do PR (ex: `123`)

Se não fornecido, marca PR da branch atual.

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
