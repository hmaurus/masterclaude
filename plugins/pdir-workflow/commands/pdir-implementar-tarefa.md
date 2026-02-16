---
description: Implementa tarefa a partir de Issue existente
argument-hint: [número-issue]
---

# PDIR: Implementar Tarefa

Implementa uma tarefa a partir de uma Issue existente no GitHub.

## Entrada

`$ARGUMENTS`: Número da Issue (ex: `42` ou `#42`)

## Instruções

### 1. Buscar Issue

```bash
gh issue view $ARGUMENTS --json number,title,body
```

**Se Issue não existir:** Informar ao usuário para criar usando `/pdir-criar-issue`.

### 2. Analisar Projeto

Entender contexto e código existente relacionado à tarefa.

**Analise criticamente se deve usar uma, mais de uma ou nenhuma das Skills abaixo (se disponíveis):**
- **localidade:** ~/.claude/plugins e ~/.claude/skills
- `/brainstorming` - Explorar abordagens e decisões de design antes de implementar
- `/feature-dev` - Desenvolvimento estruturado com foco em arquitetura
- `/frontend-design` - Para tarefas envolvendo interface/UI
- `/ui-ux-pro-max` - Guia de design com estilos, cores, fontes, UX e recomendações pesquisáveis por prioridade
- `/vercel-react-best-practices` - Guia de otimização de desempenho para aplicações React e Next.js
- `/next-best-practices` - Aplique estas regras ao escrever ou revisar código Next.js

### 3. Criar Branch

```bash
git checkout -b [tipo]/[número]-[slug]
```

**Exemplos:**
- `feat(auth): implementar login` → `feat/42-implementar-login`
- `fix(api): corrigir timeout` → `fix/15-corrigir-timeout`

### 4. Implementar Tarefa

- Planejar e Implementar a tarefa descrita na Issue.
- Esclarecer dúvidas com o usuário, se necessário.

### 5. Validações

- [ ] TypeScript sem erros (`pnpm tsc`)
- [ ] Linting passou (`pnpm lint`)
- [ ] Funcionalidade testada
- [ ] Código segue padrões do projeto

**Dica:** Se disponível, use `/webapp-testing` (skill) ou `playwright MCP` (plugin) para testes automatizados de interface, ou outras skills de teste que julgar relevantes para o tipo de tarefa.

### 6. Documentar na Issue

Registrar o que foi implementado:

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
Branch: [nome-da-branch]

Próximos passos possíveis para o usuário:
- Testar implementação
- /pdir-commit
```

## Exemplo

```bash
/pdir-implementar-tarefa 42
```
