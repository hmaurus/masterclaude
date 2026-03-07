---
description: Implementa tarefa a partir de Issue existente do GitHub com branch separada. Busca Issue, analisa projeto, cria branch, implementa, valida e documenta
argument-hint: "<número-issue> [skills: skill1, skill2, ...]"
---

# PDIR: Implementar Tarefa (com branch)

Implementa uma tarefa a partir de uma Issue do GitHub, criando branch separada.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Número da Issue:** primeiro valor numérico (ex: `42`)
- **Skills:** se contém `skills:`, extrair nomes separados por vírgula (ex: `skills: brainstorming, feature-dev`)

Se skills foram passadas, carregá-las **obrigatoriamente** antes de prosseguir.

## Instruções

### 1. Buscar Issue

```bash
gh issue view [número] --json number,title,body,comments
```

Analisar o body **e todos os comentários** — comentários frequentemente contêm decisões, esclarecimentos e requisitos adicionais.

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

### 4. Planejar Implementação

**Entrar no modo de planejamento** (usar `EnterPlanMode`) para desenhar o plano de implementação antes de escrever código. No plano:
- Listar arquivos a criar/modificar
- Descrever a abordagem técnica e decisões arquiteturais
- Identificar dependências e ordem de execução
- Considerar testes para lógica nova ou alterada

**IMPORTANTE — Passos pós-implementação no plano:** O plan mode pode limpar o contexto da conversa ao iniciar a execução. Para garantir que nenhum passo seja perdido, o plano **deve incluir obrigatoriamente** as seguintes etapas finais:
- Validar (lint, type-check, testes)
- Documentar na Issue (`gh issue comment [número]` com resumo da implementação)
- Exibir feedback final com número da issue, branch e próximos passos (`/pdir-commit`, `/pdir-criar-pr`)

Aguardar aprovação do usuário antes de prosseguir.

### 5. Implementar

Executar o plano aprovado:
- Seguir convenções do projeto (CLAUDE.md)
- Implementar de forma incremental
- Esclarecer dúvidas com o usuário antes de assumir

### 6. Validar

Executar os checks do projeto (lint, type-check, testes). Consultar `package.json`, `Makefile` ou equivalente para os comandos disponíveis.

Se algum check falhar, corrigir antes de prosseguir.

### 7. Documentar na Issue

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

### 8. Feedback Final

```
Tarefa implementada!

Issue: #[número] - [título]
Branch: [branch]

Próximos passos:
- /pdir-commit
- /pdir-criar-pr [número-issue] (se implementação completa)

Dica: execute /clear antes do próximo /pdir-implementar-tarefa-com-branch para contexto limpo.
```
