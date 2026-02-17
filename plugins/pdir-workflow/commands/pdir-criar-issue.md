---
description: Cria Issue no GitHub a partir de arquivo de tarefas ou descrição livre
argument-hint: <arquivo>#<trecho do título> | <descrição livre>
---

# PDIR: Criar Issue

Cria uma Issue no GitHub a partir de `$ARGUMENTS`.

## Formato

```bash
# Fluxo principal: referência a arquivo de tarefas (gerado por /pdir-dividir-em-tarefas)
/pdir-criar-issue docs/projeto/tarefas/lista-tarefas-setup.md#configurar eslint

# Alternativo: descrição livre
/pdir-criar-issue adicionar validação de email no cadastro
```

## Instruções

### 1. Extrair Conteúdo

**Se `$ARGUMENTS` contém `#`** → ler arquivo, buscar linha que contenha o trecho após `#` (busca parcial, case-insensitive). Extrair título, descrição e contexto da seção onde a tarefa se encontra.

**Caso contrário** → usar `$ARGUMENTS` como descrição livre. Formatar título como `type(scope): descrição curta`.

### 2. Criar Issue

Body deve ser breve — o planejamento detalhado será feito em `/pdir-implementar-tarefa`.

```bash
gh issue create \
  --title "type(scope): descrição" \
  --label "labels" \
  --milestone "milestone" \
  --body "$(cat <<'EOF'
## Descrição

[Descrição extraída ou baseada no input]

## Origem

[Arquivo: path#número | Descrição livre | Dependências: #X, #Y]
EOF
)"
```

### Labels

Inferir do título: `feat`→`enhancement`, `fix`→`bug`, `docs`→`documentation`, `chore`→`chore`, `refactor`→`refactor`, `test`→`test`. Área: `area:{scope}`.

Usar apenas labels que já existem no repositório (`gh label list --limit 100`). Não criar labels automaticamente.

### Milestone

Usar milestone existente que melhor se encaixe (`gh api repos/{owner}/{repo}/milestones`). Não criar milestones automaticamente. Omitir `--milestone` se nenhum existir.

## Feedback Final

```
Issue criada!

Issue: #[número] - [título]
Link: [url]
Labels: [labels]
Milestone: [milestone]

Próximo passo: /pdir-implementar-tarefa [número]

Dica: execute /clear antes para começar com contexto limpo.
```
