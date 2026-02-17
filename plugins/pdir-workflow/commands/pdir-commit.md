---
description: Commit e push na branch atual com Conventional Commits (feat, fix, wip, refactor, etc.) — sincroniza, commita e envia para origin
---

# PDIR: Commit

Sincroniza, commita e envia mudanças para origin.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Instruções

### 1. Verificar Estado

```bash
git status -sb
git diff --stat
```

- Tem upstream (`## branch...origin/branch`) → `git pull --ff-only`
- Branch nova (`## branch` sem `...`) → pular pull
- Sem mudanças → informar e encerrar

### 2. Criar Commit

Formato: `type(scope): descrição`

Types: `wip`, `feat`, `fix`, `docs`, `chore`, `refactor`, `style`, `test`, `perf`, `ci`, `build`

Scope: área afetada — **obrigatório**

Staging: adicionar apenas arquivos relacionados ao commit. Se houver mudanças não-relacionadas, perguntar ao usuário quais incluir.

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
