---
description: Commit e push na branch atual (suporta WIP e Conventional Commits)
---

# PDIR: Commit

Sincroniza, commita e envia mudanças para origin.

## Instruções

### 1. Verificar Estado

```bash
git status -sb
git diff --stat
```

- `## branch...origin/branch` (tem upstream) → `git pull --ff-only`
- `## branch` (sem `...`) → branch nova, pular pull
- Sem mudanças → informar e encerrar

### 2. Criar Commit

Formato: `type(scope): descrição`

Types: `wip`, `feat`, `fix`, `docs`, `chore`, `refactor`, `style`, `test`, `perf`, `ci`, `build`

Scope: área afetada — **obrigatório**

```bash
git add [arquivos específicos]

git commit -m "type(scope): descrição" \
  -m "🤖 Generated with [Claude Code](https://claude.com/claude-code)" \
  -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

### 3. Push

```bash
git push -u origin "$(git branch --show-current)"
```

Se pre-commit modificou arquivos: stage os arquivos modificados e crie um **novo commit** (nunca `--amend`).

### 4. Feedback Final

```
Commit realizado!

[hash] type(scope): descrição
Branch: [branch]

Próximos passos:
- /pdir-criar-pr (se pronto para review)
- /pdir-commit (se há mais mudanças)
```
