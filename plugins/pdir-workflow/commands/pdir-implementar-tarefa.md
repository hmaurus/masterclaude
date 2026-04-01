---
description: Implementa tarefa a partir de Issue GitHub, arquivo .md ou descrição livre, direto na branch atual
argument-hint: "<número-issue | arquivo.md | descrição livre> [skills: skill1, skill2, ...]"
---

# PDIR: Implementar Tarefa

Implementa uma tarefa direto na branch atual.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Skills:** se contém `skills:`, extrair nomes separados por vírgula (ex: `skills: brainstorming, feature-dev`). Se passadas, carregá-las **obrigatoriamente** antes de prosseguir.
- **Fonte da demanda (restante):** identificar o tipo:
  - **Número** (ex: `42`) → Issue do GitHub
  - **Caminho de arquivo** (ex: `docs/projeto/specs/spec-paywall.md`) → arquivo local
  - **Texto** → descrição livre

## Instruções

### 1. Verificar Estado do Repositório

```bash
git status -sb
git branch --show-current
```

Se houver mudanças pendentes, informar ao usuário antes de prosseguir.

### 2. Obter Escopo da Demanda

**Se Issue GitHub:**
```bash
gh issue view [número] --json number,title,body,comments
```
Analisar o body **e todos os comentários** — comentários frequentemente contêm decisões, esclarecimentos e requisitos adicionais.

**Se arquivo .md:** ler o arquivo completo como escopo.

**Se descrição livre:** usar o texto como escopo.

### 3. Analisar Projeto

Ler CLAUDE.md, README.md e arquivos relacionados à tarefa. Identificar padrões, convenções e estrutura do codebase existente.

### 4. Planejar Implementação

**Entrar no modo de planejamento** (usar `EnterPlanMode`) para desenhar o plano de implementação antes de escrever código. No plano:
- Listar arquivos a criar/modificar
- Descrever a abordagem técnica e decisões arquiteturais
- Identificar dependências e ordem de execução
- Considerar testes para lógica nova ou alterada

**IMPORTANTE — Passos pós-implementação no plano:** O plan mode pode limpar o contexto da conversa ao iniciar a execução. Para garantir que nenhum passo seja perdido, o plano **deve incluir obrigatoriamente** as seguintes etapas finais:
- Validar (lint, type-check, testes)
- Verificar contra o escopo original (reler a fonte da demanda e confirmar que todos os pontos foram atendidos)
- Smoke test visual: navegar pelas rotas afetadas e verificar se não há erros no console
- Se a fonte foi Issue: documentar na Issue e perguntar se deseja fechá-la
- Exibir feedback final com fonte, branch e próximos passos

Aguardar aprovação do usuário antes de prosseguir.

### 5. Implementar

Executar o plano aprovado:
- Seguir convenções do projeto (CLAUDE.md)
- Implementar de forma incremental
- Esclarecer dúvidas com o usuário antes de assumir

### 6. Validar

**CI:** Executar os checks do projeto (lint, type-check, testes). Consultar `package.json`, `Makefile` ou equivalente para os comandos disponíveis. Se algum check falhar, corrigir antes de prosseguir.

**Spec check:** Reler a fonte da demanda (Issue, arquivo .md ou descrição) e verificar item por item se todos os pontos foram atendidos. Se algo ficou faltando, implementar antes de prosseguir.

**Smoke test:** Navegar pelas rotas afetadas, verificar se não há erros no console e se o comportamento está correto visualmente.

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

Perguntar ao usuário se deseja fechar a issue agora.

Se sim:
```bash
gh issue close [número] --comment "Fechada via implementação direta (sem PR)."
```

Se não: informar que a issue permanece aberta.

### 8. Feedback Final

```
Tarefa implementada!

Fonte: [#número - título | arquivo | descrição]
Branch atual: [branch]

Próximos passos:
- /pdir-commit

Dica: para implementar com branch separada, use /pdir-implementar-tarefa-com-branch.
```
