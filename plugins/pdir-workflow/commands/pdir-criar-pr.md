---
description: Cria Pull Request vinculado a uma Issue do GitHub. Verifica estado da branch, faz push se necessário, busca dados da Issue e gera PR com Conventional Commits
argument-hint: <número-da-issue>
---

# PDIR: Criar PR

Cria Pull Request vinculado a uma Issue.

**Pré-requisitos:** estar em branch de feature (não main), commits já realizados (`/pdir-commit`).

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair número da Issue de `$ARGUMENTS` (ex: `42` ou `#42`).

Se `$ARGUMENTS` vazio, tentar extrair do nome da branch (ex: `feat/42-login` → Issue `#42`). Se não conseguir, perguntar ao usuário.

## Instruções

### 1. Verificar Estado

```bash
git branch --show-current
git status -sb
```

Se estiver na main: informar erro e encerrar.
Se houver mudanças não commitadas: informar e sugerir `/pdir-commit` primeiro.

### 2. Push (se necessário)

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

Se não tem upstream:

```bash
git push -u origin "$(git branch --show-current)"
```

### 3. Buscar Issue e Analisar Branch

```bash
gh issue view [número] --json number,title,body
git log main..HEAD --oneline
git diff main --stat
```

Derivar `type` do prefixo da branch (ex: `feat/` → `feat`, `fix/` → `fix`). Derivar título e resumo a partir da Issue e dos commits.

### 4. Criar Pull Request

```bash
gh pr create \
  --title "type(scope): descrição derivada da Issue" \
  --body "$(cat <<'EOF'
Closes #[número-da-issue]

## Resumo

[Breve resumo derivado da Issue e dos commits]

## Mudanças Principais

- [Mudança 1]
- [Mudança 2]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 5. Feedback Final

```
PR criado!

PR: #[número-do-pr]
Branch: [branch]
Link: [url]

Próximos passos:
- /pdir-merge-tarefa (quando aprovado)
- /pdir-commit (se continuar desenvolvendo)
```
