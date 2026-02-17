---
description: Implementa tarefa a partir de Issue existente
argument-hint: <número-issue> [/skill1 /skill2 ...]
---

# PDIR: Implementar Tarefa

Implementa uma tarefa a partir de uma Issue do GitHub.

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Número da Issue:** primeiro valor numérico (ex: `42`)
- **Skills:** palavras começando com `/` (ex: `/brainstorming /feature-dev`)

Se skills foram passadas, carregá-las **obrigatoriamente** antes de prosseguir.

## Instruções

### 1. Buscar Issue

```bash
gh issue view [número] --json number,title,body
```

Se não existir: informar para criar usando `/pdir-criar-issue`.

### 2. Analisar Projeto

Ler arquivos relacionados à tarefa, identificar padrões e convenções do codebase existente.

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
gh issue comment [número] --body "$(cat <<'EOF'
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
- /pdir-commit
- /pdir-criar-pr [número-issue] (se implementação completa)
```
