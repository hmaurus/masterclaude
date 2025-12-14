---
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

Analise o conteúdo de `$ARGUMENTS`:

1. **Se contém `.md#`** → extrair arquivo e número da tarefa
2. **Se contém `.md` seguido de texto entre aspas** → extrair arquivo e buscar tarefa pelo texto
3. **Caso contrário** → tratar como descrição livre

## Extrair de Arquivo de Tarefas

Ao referenciar arquivo:

1. Localizar o arquivo (usar Glob se caminho parcial)
2. Ler o arquivo markdown
3. Localizar a seção da tarefa (pelo número `## N.` ou texto parcial do título)
4. Extrair: título formatado, descrição e dependências

## Formatar Título

- Se extraído de arquivo: usar título já formatado (`type(scope): descrição`)
- Se prompt livre: identificar tipo (`feat`, `fix`, `refactor`, `docs`, `chore`, `test`) e escopo

## Criar Issue

```bash
gh issue create \
  --title "type(scope): descrição" \
  --body "Descrição extraída ou baseada no input."
```

**Nota:** O body deve ser breve. O planejamento detalhado será feito em `/pdir-implementar-tarefa`.

## Feedback Final

```
Issue criada!

Issue: #[número] - [título]
Link: [url]

Próximo passo: /pdir-implementar-tarefa [número]
```
