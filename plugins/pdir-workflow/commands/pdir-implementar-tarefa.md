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
