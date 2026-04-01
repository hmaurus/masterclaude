---
description: Finaliza PR fazendo squash merge, deletando branch e sincronizando local. Usar quando o PR está aprovado e pronto para merge
argument-hint: [numero-do-pr]
---

# PDIR: Merge PR

Valida, faz merge do PR e limpa branch local/remota.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

`$ARGUMENTS` (opcional): número do PR. Se não fornecido, usa PR da branch atual.

## Instruções

### 1. Validação Local

Executar os checks do projeto (lint, type-check, build). Consultar `package.json`, `Makefile` ou equivalente para os comandos disponíveis.

Se algum check falhar, parar e informar ao usuário.

### 2. Verificar CI

```bash
gh pr checks $ARGUMENTS
```

Se houver checks falhando, parar e perguntar ao usuário se deseja aguardar, prosseguir mesmo assim, ou abortar.

### 3. Fazer Merge

```bash
gh pr merge $ARGUMENTS --squash --delete-branch
```

### 4. Sincronizar Local

```bash
FEATURE_BRANCH=$(git branch --show-current)
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull origin "$DEFAULT_BRANCH"
git branch -d "$FEATURE_BRANCH"
```

### 5. Feedback Final

```
Merge realizado!

PR: #[número] → [branch-default] (squash merge)
Branch deletada (local + remota)

Próximos passos:
- /pdir-deploy (se pronto para produção)
- /pdir-proxima-demanda (sugerir próxima demanda)
```
