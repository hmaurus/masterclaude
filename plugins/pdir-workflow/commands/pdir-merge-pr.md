---
description: Finaliza PR fazendo squash merge, deletando branch e sincronizando local. Usar quando o PR está aprovado e pronto para merge
argument-hint: [numero-do-pr]
---

# PDIR: Merge PR

Valida, faz o squash merge do PR e limpa a branch local/remota.

**Pré-requisito:** PR aprovado e pronto para merge.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Descobrir o PR

- **Com argumento** (`$ARGUMENTS`): número do PR (descarte o `#` se vier).
- **Sem argumento:** use o PR aberto da branch atual.

Leia o PR com `gh pr view <número> --json number,title,state,isDraft,headRefName` e **mostre número + título** — é a conferência de que você vai mergear o PR certo. Um squash merge com `--delete-branch` é irreversível na prática (some com a branch). Se o PR não estiver aberto (já mergeado/fechado) ou for draft, **pare e avise** — não faça merge.

## Instruções

### 1. Validar localmente

Rode os checks do projeto (lint, type-check, build) — consulte `package.json`, `Makefile` ou equivalente para os comandos disponíveis. Se algum falhar, pare e informe ao usuário.

### 2. Verificar o CI do PR

Cheque o status dos checks de CI do PR (`gh pr checks <número>`). Se houver algo falhando, pare e pergunte se o usuário quer aguardar, seguir mesmo assim, ou abortar.

### 3. Fazer o merge

Guarde o nome da branch de origem do PR — o `headRefName` que você leu ao descobrir o PR. Precisa dele para a limpeza, e a branch pode sumir logo em seguida.

Faça o squash merge deletando a branch:

```bash
gh pr merge <número> --squash --delete-branch
```

O `--squash` (convenção do PDIR: um commit por PR) e o `--delete-branch` (remove a branch remota — e a local, se você estiver nela) são intencionais — mantenha ambos.

### 4. Sincronizar o local

Volte para o branch default e atualize-o:

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull origin "$DEFAULT_BRANCH"
```

O passo anterior já removeu a branch de origem remota (e a local, se você estava nela). Se a branch local ainda existir, remova-a com `git branch -d <headRefName>`. O `-d` recusa apagar trabalho não mergeado — se ele reclamar, **não** force com `-D`: investigue por que a branch parece não mergeada.

### 5. Feedback final

Informe ao usuário:

```
Merge realizado!

PR: #<número> → <branch-default> (squash merge)
Branch deletada (local + remota)

Próximos passos:
- /pdir-deploy (se pronto para produção)
- /pdir-proxima-demanda (sugerir próxima demanda)
```
