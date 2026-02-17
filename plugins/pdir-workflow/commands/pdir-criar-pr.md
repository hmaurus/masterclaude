---
description: Cria Pull Request vinculado a uma Issue do GitHub. Extrai Issue da branch automaticamente ou recebe número explícito
argument-hint: [número-da-issue]
---

# PDIR: Criar PR

Cria Pull Request vinculado a uma Issue.

**Pré-requisitos:** estar em branch de feature (não main), commits já realizados (`/pdir-commit`).

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

**Fluxo principal (sem argumento):** extrair número da Issue do nome da branch atual. O formato esperado é `tipo/numero-slug` (ex: `feat/42-login` → Issue `#42`). Extrair o primeiro número encontrado após a `/`.

**Fluxo alternativo (com argumento):** usar número da Issue de `$ARGUMENTS` (ex: `42` ou `#42`).

Se não conseguir extrair de nenhuma forma, perguntar ao usuário.

## Formato

```bash
# Fluxo principal: extrai Issue da branch automaticamente
/pdir-criar-pr

# Alternativo: número explícito
/pdir-criar-pr 42
```

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

Se tem upstream mas há commits locais não enviados (`git log @{u}..HEAD --oneline`), fazer `git push`.

### 3. Buscar Issue e Analisar Branch

```bash
gh issue view [número] --json number,title,body
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git log "$DEFAULT_BRANCH"..HEAD --oneline
git diff "$DEFAULT_BRANCH" --stat
```

Se a Issue não existir: informar erro com o número tentado e perguntar ao usuário o número correto.

Derivar `type` do prefixo da branch (ex: `feat/` → `feat`, `fix/` → `fix`). Derivar `scope` do título da Issue ou da área principal dos arquivos modificados. Derivar título e resumo a partir da Issue e dos commits.

### 4. Criar Pull Request

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
gh pr create \
  --base "$DEFAULT_BRANCH" \
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
