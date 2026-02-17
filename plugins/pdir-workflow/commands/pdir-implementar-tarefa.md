---
description: Implementa tarefa a partir de Issue existente
argument-hint: <número-issue>
---

# PDIR: Implementar Tarefa

Implementa uma tarefa a partir de uma Issue do GitHub.

## Instruções

### 1. Buscar Issue

```bash
gh issue view $ARGUMENTS --json number,title,body
```

Se não existir: informar para criar usando `/pdir-criar-issue`.

### 2. Analisar Projeto

Ler arquivos relacionados à tarefa, identificar padrões e convenções do codebase existente. Verificar skills disponíveis que possam ser relevantes ao tipo de tarefa (ex: brainstorming, feature-dev, frontend-design, testing).

### 3. Criar Branch

```bash
git checkout -b [tipo]/[número]-[slug]
```

Exemplo: `feat(auth): implementar login` → `feat/42-implementar-login`

### 4. Implementar

Planejar e implementar a tarefa descrita na Issue. Esclarecer dúvidas com o usuário se necessário.

### 5. Validar

Executar os checks do projeto (lint, type-check, testes). Consultar `package.json`, `Makefile` ou equivalente para os comandos disponíveis.

### 6. Documentar na Issue

```bash
gh issue comment $ARGUMENTS --body "$(cat <<'EOF'
## Implementação Realizada

### Arquivos modificados/criados
- `arquivo.ts` - descrição

### Resumo
Breve descrição do que foi feito.
EOF
)"
```

### 7. Feedback Final

```
Tarefa implementada!

Issue: #[número] - [título]
Branch: [branch]

Próximos passos:
- Testar implementação
- /pdir-commit
```
