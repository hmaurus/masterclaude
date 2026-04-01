---
description: Implementa tarefa a partir de Issue GitHub, arquivo .md ou descrição livre, com branch separada
argument-hint: "<número-issue | arquivo.md | descrição livre> [skills: skill1, skill2, ...]"
---

# PDIR: Implementar Tarefa (com branch)

Implementa uma tarefa criando branch separada.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Skills:** se contém `skills:`, extrair nomes separados por vírgula (ex: `skills: brainstorming, feature-dev`). Se passadas, carregá-las **obrigatoriamente** antes de prosseguir.
- **Fonte da demanda (restante):** identificar o tipo:
  - **Número** (ex: `42`) → Issue do GitHub
  - **Caminho de arquivo** (ex: `docs/projeto/specs/spec-paywall.md`) → arquivo local
  - **Texto** → descrição livre

## Instruções

### 1. Obter Escopo da Demanda

**Se Issue GitHub:**
```bash
gh issue view [número] --json number,title,body,comments
```
Analisar o body **e todos os comentários** — comentários frequentemente contêm decisões, esclarecimentos e requisitos adicionais.

**Se arquivo .md:** ler o arquivo completo como escopo.

**Se descrição livre:** usar o texto como escopo.

### 2. Analisar Projeto

Ler CLAUDE.md, README.md e arquivos relacionados à tarefa. Identificar padrões, convenções e estrutura do codebase existente.

### 3. Criar Branch

Verificar estado atual:

```bash
git status -sb
git branch --show-current
```

Se houver mudanças pendentes, informar ao usuário antes de prosseguir.

Derivar `tipo` do escopo da demanda: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.

```bash
git checkout -b [tipo]/[número-ou-slug]
```

Slug: palavras-chave do título em kebab-case, sem acentos, max 50 chars.

Exemplos:
- Issue `#42 feat(auth): implementar login` → `feat/42-implementar-login`
- Arquivo `spec-paywall.md` → `feat/paywall`
- Descrição `corrigir link quebrado` → `fix/link-quebrado`

### 4. Planejar Implementação

**Entrar no modo de planejamento** (usar `EnterPlanMode`) para desenhar o plano de implementação antes de escrever código. No plano:
- Listar arquivos a criar/modificar
- Descrever a abordagem técnica e decisões arquiteturais
- Identificar dependências e ordem de execução
- Considerar testes para lógica nova ou alterada

**IMPORTANTE — Passos pós-implementação no plano:** O plan mode pode limpar o contexto da conversa ao iniciar a execução. Para garantir que nenhum passo seja perdido, o plano **deve incluir obrigatoriamente** as seguintes etapas finais:
- Validar com `/pdir-validar-implementacao` (CI + spec check + smoke test)
- Se a fonte foi Issue: documentar na Issue
- Exibir feedback final com fonte, branch e próximos passos (`/pdir-commit`, `/pdir-criar-pr`)

Aguardar aprovação do usuário antes de prosseguir.

### 5. Implementar

Executar o plano aprovado:
- Seguir convenções do projeto (CLAUDE.md)
- Implementar de forma incremental
- Esclarecer dúvidas com o usuário antes de assumir

### 6. Validar

Executar `/pdir-validar-implementacao` passando a mesma fonte da demanda. Se a validação reportar falhas, corrigir antes de prosseguir.

### 7. Documentar na Issue (se aplicável)

**Apenas se a fonte foi uma Issue do GitHub:**

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

Fonte: [#número - título | arquivo | descrição]
Branch: [branch]

Próximos passos:
- /pdir-commit
- /pdir-criar-pr (se implementação completa)

Dica: execute /clear antes do próximo /pdir-implementar-tarefa-com-branch para contexto limpo.
```
