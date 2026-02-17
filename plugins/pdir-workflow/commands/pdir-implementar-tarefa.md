---
description: Implementa tarefa a partir de Issue existente do GitHub. Busca Issue, analisa projeto, cria branch, implementa, valida e documenta
argument-hint: <número-issue> [skills: skill1, skill2, ...]
---

# PDIR: Implementar Tarefa

Implementa uma tarefa a partir de uma Issue do GitHub.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Número da Issue:** primeiro valor numérico (ex: `42`)
- **Skills:** se contém `skills:`, extrair nomes separados por vírgula (ex: `skills: brainstorming, feature-dev`)

Se skills foram passadas, carregá-las **obrigatoriamente** antes de prosseguir.

## Instruções

### 1. Buscar Issue

```bash
gh issue view [número] --json number,title,body
```

Se não existir: informar para criar usando `/pdir-criar-issue`.

### 2. Analisar Projeto

Ler CLAUDE.md, README.md e arquivos relacionados à tarefa. Identificar padrões, convenções e estrutura do codebase existente.

### 3. Criar Branch

Verificar estado atual:

```bash
git status -sb
git branch --show-current
```

Se houver mudanças pendentes, informar ao usuário antes de prosseguir.

Derivar `tipo` do título da Issue: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.

```bash
git checkout -b [tipo]/[número]-[slug]
```

Slug: palavras-chave do título em kebab-case, sem acentos, max 50 chars.

Exemplo: `feat(auth): implementar login` → `feat/42-implementar-login`

### 4. Implementar

Planejar e implementar a tarefa descrita na Issue:
- Seguir convenções do projeto (CLAUDE.md)
- Implementar de forma incremental
- Esclarecer dúvidas com o usuário antes de assumir
- Considerar testes para lógica nova ou alterada

### 5. Validar

Executar os checks do projeto (lint, type-check, testes). Consultar `package.json`, `Makefile` ou equivalente para os comandos disponíveis.

Se algum check falhar, corrigir antes de prosseguir.

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

Dica: execute /clear antes do próximo /pdir-implementar-tarefa para contexto limpo.
```
