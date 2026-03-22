---
description: Faz deploy para produção via merge da branch atual para a branch de produção (main). Consulta CLAUDE.md do projeto para determinar o fluxo de deploy.
---

# PDIR: Deploy

Faz deploy para produção via merge para a branch de produção.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Instruções

### 1. Identificar Fluxo de Deploy

Ler CLAUDE.md do projeto para identificar:
- Branch de trabalho (ex: `develop`)
- Branch de produção (ex: `main`)
- Método de deploy (CI/CD automático em push, manual via `gh workflow run`, etc.)

Se não houver documentação de deploy, perguntar ao usuário.

### 2. Verificar Estado

```bash
git status -sb
git branch --show-current
```

- Se houver mudanças pendentes: informar e perguntar se deve commitar antes (sugerir `/pdir-commit`)
- Se não estiver na branch de trabalho: informar e perguntar como prosseguir

### 3. Sincronizar

```bash
git pull --ff-only
```

### 4. Merge para Produção

```bash
git checkout [branch-producao]
git merge [branch-trabalho] --no-edit
git push origin [branch-producao]
```

### 5. Voltar para Branch de Trabalho

```bash
git checkout [branch-trabalho]
```

### 6. Verificar Deploy (se CI/CD)

Se o projeto usa CI/CD automático, verificar o status do workflow:

```bash
gh run list --limit 1 --json status,conclusion,databaseId
```

Se o deploy falhar, informar o erro ao usuário.

### 7. Feedback Final

```
Deploy iniciado!

Merge: [branch-trabalho] → [branch-producao]
Branch atual: [branch-trabalho]
Deploy: [método — ex: CI/CD automático, gh workflow run, etc.]

Próximos passos:
- /pdir-commit (continuar trabalhando)
```
