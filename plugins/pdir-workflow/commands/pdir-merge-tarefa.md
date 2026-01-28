---
description: Valida, faz merge e limpa branch
argument-hint: [pr-number]
---

# PDIR: Merge Tarefa

Valida, faz merge do PR e limpa branch local/remota.

## Entrada

`$ARGUMENTS` (opcional): Número do PR (ex: `123`)

Se não fornecido, usa PR da branch atual.

## Instruções

### 0. Pre-Review (Opcional)

Antes do merge, considere executar uma revisão:
- `/code-review` - Revisão de código do PR
- `/pr-review-toolkit:review-pr` - Revisão abrangente com agentes especializados

### 1. Validação Final

```bash
pnpm check
pnpm lint
pnpm build
```

### 2. Fazer Merge

```bash
gh pr merge $ARGUMENTS --squash --delete-branch
```

**Nota:** `--delete-branch` já deleta branch remota e local.

### 3. Sincronizar Local

```bash
git checkout main
git pull origin main
```

### 4. Feedback Final

```
Merge realizado!

PR: #[número] → main
Branch deletada

Tarefa concluída!
```

## Checklist

**Antes do merge:**
- [ ] Checks passaram

**Após merge:**
- [ ] Issue fechada
- [ ] Main atualizada

## Exemplo

```bash
/pdir-merge-tarefa        # PR da branch atual
/pdir-merge-tarefa 123    # PR específico
```
