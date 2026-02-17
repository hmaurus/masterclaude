---
name: pdir-criar-issue
description: Cria Issue a partir de descrição livre ou referência a arquivo de tarefas
argument-hint: [descrição] | [arquivo]#[número] | [arquivo] "[texto]"
---

# PDIR: Criar Issue

Cria uma Issue no GitHub a partir de `$ARGUMENTS`.

## Formas de Uso

### 1. Prompt Livre

```bash
/pdir-criar-issue adicionar validação de email no cadastro
```

### 2. Referência por Número

```bash
/pdir-criar-issue docs/projeto/tarefas/lista-tarefas-setup-configuracao.md#1
```

### 3. Referência por Texto

```bash
/pdir-criar-issue lista-tarefas-setup-configuracao.md "inicializar projeto"
```

## Interpretar $ARGUMENTS

Analise o conteúdo de `$ARGUMENTS` para extrair o conteúdo da tarefa específica:

1. **Se contém `.md#`** → no arquivo, buscar tarefa pelo número
2. **Se contém `.md` seguido de texto entre aspas** → no arquivo, buscar tarefa pelo texto
3. **Caso contrário** → tratar como descrição livre

## Extrair de Arquivo de Tarefas

Ao referenciar arquivo:

1. Localizar o arquivo (usar Glob se caminho parcial)
2. Ler o arquivo markdown
3. Localizar a seção da tarefa:
   - **Por número:** contar os headings `##` do corpo (excluindo seções auxiliares como "Ordem de Implementação") — o N-ésimo `##` corresponde à tarefa N
   - **Por texto:** busca parcial no título do heading `##`
4. Extrair: título (já no formato `type(scope): descrição` se gerado por `/pdir-dividir-em-tarefas`), descrição e dependências

## Formatar Título

- **Se já estiver no formato `type(scope): descrição`:** preservar como está
- **Caso contrário:** identificar tipo (`feat`, `fix`, `refactor`, `docs`, `chore`, `test`) e escopo a partir do contexto da tarefa

## Criar Issue

```bash
gh issue create \
  --title "type(scope): descrição" \
  --label "labels" \
  --body "$(cat <<'EOF'
## Descrição

[Descrição extraída ou baseada no input]

## Origem

[Prompt livre | Arquivo: path#número | Dependências: #X, #Y]
EOF
)"
```

### Labels

Toda issue deve ter pelo menos uma label de **tipo** e uma de **área**.

1. Inferir do contexto da tarefa:
   - **Tipo** (pelo `type` do título): `feat` → `enhancement`, `fix` → `bug`, `docs` → `documentation`, `chore` → `chore`, `refactor` → `refactor`, `test` → `test`
   - **Área** (pelo `scope` ou contexto): `area:frontend`, `area:backend`, `area:database`, `area:auth`, `area:infra`, etc.
2. Verificar se as labels existem: `gh label list --limit 100`
3. Criar as que não existirem:

```bash
gh label create "nome-da-label" --description "Descrição" --color "HEXCOR"
```

### Milestone

Toda issue deve ter um milestone associado.

1. Inferir a fase/milestone mais adequada com base no contexto da tarefa
2. Verificar milestones existentes: `gh api repos/{owner}/{repo}/milestones`
3. Se o milestone não existir, criar:

```bash
gh api repos/{owner}/{repo}/milestones --method POST -f title="Nome do Milestone"
```

4. Adicionar `--milestone "nome"` ao `gh issue create`

**Nota:** O body deve ser breve. O planejamento detalhado será feito em `/pdir-implementar-tarefa`.

## Problemas Comuns

- **gh não autenticado:** executar `gh auth login`
- **Repositório sem remote:** executar `gh repo set-default`

## Feedback Final

```
Issue criada!

Issue: #[número] - [título]
Link: [url]
Labels: [labels aplicadas]
Milestone: [milestone associado]

Próximo passo: /pdir-implementar-tarefa [número]

Dica: execute /clear antes para começar com contexto limpo.
```
