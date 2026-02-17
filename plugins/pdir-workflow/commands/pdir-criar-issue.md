---
description: Cria Issue no GitHub com labels (cria automaticamente se não existirem) e milestone inferidos, a partir de arquivo de tarefas (gerado por /pdir-dividir-em-tarefas) ou descrição livre
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

### 2. Resolver Labels e Milestone

```bash
gh label list --limit 100
gh api repos/{owner}/{repo}/milestones
```

**Labels:** inferir do título usando o mapeamento abaixo. Se a label inferida já existir, usar. Se não existir, **criar automaticamente** com `gh label create`:

| Type | Label | Cor | Descrição |
|------|-------|-----|-----------|
| `feat` | `enhancement` | `#a2eeef` | New feature or request |
| `fix` | `bug` | `#d73a4a` | Something isn't working |
| `docs` | `documentation` | `#0075ca` | Improvements or additions to documentation |
| `chore` | `chore` | `#ededed` | Maintenance tasks |
| `refactor` | `refactor` | `#d4c5f9` | Code refactoring |
| `test` | `test` | `#bfd4f2` | Testing related |
| `perf` | `performance` | `#f9d0c4` | Performance improvements |
| `ci` | `ci/cd` | `#e4e669` | CI/CD pipeline |
| `style` | `style` | `#c5def5` | Code style and formatting |

**Área:** `area:{scope}` — mesma regra: usar se existir, criar se não existir (cor `#5319e7`).

Para types sem mapeamento definido, omitir label de tipo.

```bash
# Exemplo de criação automática de label
gh label create "enhancement" --color "a2eeef" --description "New feature or request"
```

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
