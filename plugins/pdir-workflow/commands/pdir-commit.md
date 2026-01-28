---
description: Commit e push na branch atual (suporta WIP e Conventional Commits)
---

# PDIR: Commit

Sincroniza, commita e envia mudanças para origin.

## Instruções

### 1. Sincronizar e Verificar

Informações da branch:
!`git status -sb`
!`git diff --stat`

**Interpretar saída do `git status -sb`:**
- `## main...origin/main` → tem upstream, execute `git pull --ff-only`
- `## main` (sem `...`) → branch nova, pule o pull

**Se não houver mudanças:** Informar e encerrar.

### 2. Criar Commit

Formato: `tipo(escopo): descrição`

**Tipos:** `wip`, `feat`, `fix`, `docs`, `chore`, `refactor`, `style`, `test`, `perf`, `ci`, `build`

**Escopo:** área afetada (`auth`, `api`, `ui`, `db`, etc.) - **obrigatório**

```bash
git add [arquivos específicos]

git commit -m "$(cat <<'EOF'
tipo(escopo): descrição

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 3. Push

```bash
git push -u origin "$(git branch --show-current)"
```

### 4. Feedback Final

```
Commit realizado!

[hash] tipo(escopo): descrição
Branch: [branch]

Próximos passos:
- /pdir-criar-pr (se pronto para review)
- /pdir-commit (se há mais mudanças)
```

## Problemas Comuns

**Pre-commit modificou arquivos:**
```bash
git add [arquivos modificados pelo hook] && git commit --amend --no-edit && git push --force-with-lease
```

**Push rejeitado:**
```bash
git pull --rebase && git push
```
