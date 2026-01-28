---
description: Cria Pull Request para a branch atual
---

# PDIR: Criar PR

Cria Pull Request para a branch atual.

**Pré-requisitos:**
- Estar em branch de feature (não main)
- Commits já realizados (`/pdir-commit`)
- Issue criada

## Instruções

### 1. Verificar Estado

```bash
git branch --show-current
git status
```

**Se estiver na main:** Informar erro e encerrar.

### 2. Push

```bash
git push -u origin "$(git branch --show-current)"
```

### 3. Criar Pull Request

```bash
gh pr create \
  --title "tipo(escopo): descrição" \
  --body "$(cat <<'EOF'
Closes #[número-da-issue]

## Resumo

[Breve resumo do que foi implementado]

## Mudanças Principais

- [Mudança 1]
- [Mudança 2]

## Checklist

- [x] Código segue padrões do projeto
- [x] Funcionalidade testada

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 4. Confirmar

Informar ao usuário:
```
PR criado!

Branch: [nome-da-branch]
PR: #[número-do-pr]

Próximos passos:
1. Continue desenvolvendo com `/pdir-commit`
2. `/pdir-merge-tarefa` quando pronto para merge
```

## Resolução de Problemas

**Push falhou (conflito):**
```bash
git pull origin main --rebase
git push origin "$(git branch --show-current)"
```

**PR já existe:**
```bash
gh pr view  # ver PR existente
```
