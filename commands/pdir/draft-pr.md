---
description: Cria Draft Pull Request (commits já devem estar feitos)
---

# PDIR: Criar Draft PR

Cria Draft Pull Request para a branch atual.

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

### 3. Criar Draft Pull Request

```bash
gh pr create --draft \
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
Draft PR criado!

Branch: [nome-da-branch]
PR: #[número-do-pr] (Draft)

Próximos passos:
1. Continue desenvolvendo com `/pdir-commit`
2. `/pdir-ready-pr` quando pronto
3. `/pdir-merge-tarefa` para merge
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
