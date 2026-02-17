---
description: Cria Issue no GitHub com labels e milestone inferidos, a partir de arquivo de tarefas (gerado por /pdir-dividir-em-tarefas) ou descrição livre
argument-hint: <arquivo>#<trecho do título> ou <descrição livre>
---

# PDIR: Criar Issue

Cria uma Issue no GitHub a partir de `$ARGUMENTS`.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

**Se contém `#`** → separar em `arquivo` (antes do `#`) e `trecho` (após o `#`).

**Caso contrário** → tratar como descrição livre.

## Formato

```bash
# Fluxo principal: referência a arquivo de tarefas (gerado por /pdir-dividir-em-tarefas)
/pdir-criar-issue docs/projeto/tarefas/lista-tarefas-setup.md#configurar eslint

# Alternativo: descrição livre
/pdir-criar-issue adicionar validação de email no cadastro
```

## Instruções

### 1. Extrair Conteúdo

**Se referência a arquivo** → ler arquivo, buscar linha que contenha o trecho (busca parcial, case-insensitive). Extrair título, descrição e contexto da seção.

**Se descrição livre** → formatar título como `type(scope): descrição curta`.

### 2. Buscar Labels e Milestones Existentes

```bash
gh label list --limit 100
gh api repos/{owner}/{repo}/milestones
```

**Labels:** inferir do título: `feat`→`enhancement`, `fix`→`bug`, `docs`→`documentation`, `chore`→`chore`, `refactor`→`refactor`, `test`→`test`. Área: `area:{scope}`. Usar apenas labels que já existem. Não criar labels.

**Milestone:** usar milestone existente que melhor se encaixe. Não criar milestones. Omitir `--milestone` se nenhum existir.

### 3. Criar Issue

Body deve ser breve — o planejamento detalhado será feito em `/pdir-implementar-tarefa`.

```bash
gh issue create \
  --title "type(scope): descrição" \
  --label "label1" --label "label2" \
  --milestone "milestone" \
  --body "$(cat <<'EOF'
## Descrição

[Descrição extraída ou baseada no input]

## Origem

[Arquivo: path#número | Descrição livre | Dependências: #X, #Y]
EOF
)"
```

## Feedback Final

```
Issue criada!

Issue: #[número] - [título]
Link: [url]
Labels: [labels]
Milestone: [milestone] (se aplicável)

Próximos passos:
- /pdir-implementar-tarefa [número]

Dica: execute /clear antes para começar com contexto limpo.
```
