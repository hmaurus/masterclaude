---
description: Cria Pull Request para a branch atual
argument-hint: <número-da-issue>
---

# PDIR: Criar PR

Cria Pull Request vinculado a uma Issue.

**Pré-requisitos:** estar em branch de feature (não main), commits já realizados (`/pdir-commit`).

## Instruções

### 1. Verificar Estado

```bash
git branch --show-current
git status
```

Se estiver na main: informar erro e encerrar.

### 2. Push (se necessário)

Verificar se branch já tem upstream. Se não:

```bash
git push -u origin "$(git branch --show-current)"
```

### 3. Buscar Issue

`$ARGUMENTS`: número da Issue (ex: `42` ou `#42`).

```bash
gh issue view $ARGUMENTS --json number,title,body
```

Derivar título do PR a partir do título da Issue.

### 4. Criar Pull Request

```bash
gh pr create \
  --title "type(scope): descrição derivada da Issue" \
  --body "$(cat <<'EOF'
Closes #[número-da-issue]

## Resumo

[Breve resumo do que foi implementado]

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

Branch: [branch]
PR: #[número-do-pr]

Próximos passos:
- /pdir-merge-tarefa (quando aprovado)
- /pdir-commit (se continuar desenvolvendo)
```
