---
description: Valida, faz squash merge do PR e limpa branch
argument-hint: [pr-number]
---

# PDIR: Merge Tarefa

Valida, faz merge do PR e limpa branch local/remota.

## Entrada

`$ARGUMENTS` (opcional): número do PR. Se não fornecido, usa PR da branch atual.

## Instruções

### 1. Pre-Review (Opcional)

Se disponível, considerar executar `/code-review` antes do merge.

### 2. Validação Final

Executar os checks do projeto (lint, type-check, build). Consultar `package.json`, `Makefile` ou equivalente para os comandos disponíveis.

### 3. Verificar CI

```bash
gh pr checks $ARGUMENTS
```

Se houver checks falhando, informar ao usuário antes de prosseguir.

### 4. Fazer Merge

```bash
gh pr merge $ARGUMENTS --squash --delete-branch
```

### 5. Sincronizar Local

```bash
git checkout main
git pull origin main
```

### 6. Feedback Final

```
Merge realizado!

PR: #[número] → main
Branch deletada

Tarefa concluída!
```
