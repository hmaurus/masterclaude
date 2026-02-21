---
description: Analisa contexto atual e projeto para sugerir a próxima tarefa. Ideal para usar após implementar uma tarefa, antes do /clear
argument-hint: [arquivo-prd-ou-tarefas]
---

# PDIR: Próxima Tarefa

Analisa o contexto da sessão atual, o plano do projeto e as Issues do GitHub para sugerir a próxima tarefa a implementar. Ideal para ser executado logo após concluir uma tarefa, aproveitando o contexto fresco antes do `/clear`.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

`$ARGUMENTS` (opcional): caminho para PRD ou arquivo de tarefas. Se não fornecido, usar `docs/projeto/PRD.md` como padrão.

## Formato

```bash
# Sem argumento: usa docs/projeto/PRD.md como referência
/pdir-proxima-tarefa

# Com arquivo específico
/pdir-proxima-tarefa docs/projeto/PRD.md
/pdir-proxima-tarefa docs/projeto/tarefas/lista-tarefas-setup.md
```

## Instruções

### 1. Analisar Contexto da Sessão Atual

Resumir brevemente o que foi feito nesta sessão:
- Qual tarefa/issue foi implementada
- Quais arquivos foram criados ou modificados
- Qual área do projeto foi alterada (ex: auth, API, UI, infra)

Este resumo será usado para inferir dependências e prioridades da próxima tarefa.

### 2. Buscar Plano do Projeto

**Se `$ARGUMENTS` fornecido** → usar como caminho do documento.

**Se não** → usar `docs/projeto/PRD.md`.

Se o arquivo existir, ler e buscar seções que contenham etapas, fases, roadmap, checklist ou lista de tarefas. Identificar:
- Tarefas já concluídas (marcadas com ✅, [x], ou similar)
- Tarefas pendentes
- Ordem de prioridade/dependência

Se o arquivo não existir, pular para o passo 3.

### 3. Verificar Issues no GitHub

```bash
# Issues abertas (candidatas para próxima tarefa)
gh issue list --state open --limit 30 --json number,title,labels

# Issues fechadas recentemente (para entender progresso)
gh issue list --state closed --limit 10 --json number,title
```

Cruzar com o PRD (se disponível) para identificar:
- Tarefas do PRD que já têm Issue criada
- Tarefas do PRD que ainda não têm Issue
- Issues abertas que não estão no PRD (extras)

### 4. Sugerir Próxima Tarefa

Considerar os seguintes critérios para a sugestão:
- **Dependências:** o que a tarefa recém-implementada desbloqueou
- **Ordem lógica:** seguir a sequência do PRD/etapas
- **Não duplicar:** evitar sugerir tarefas que já têm Issue aberta
- **Prioridade natural:** infra/config → modelos/types → lógica de negócio → API → UI → testes de integração/E2E

Apresentar a sugestão com:
- **Título** no formato `type(scope): descrição curta`
- **Justificativa** breve de por que esta é a próxima tarefa lógica
- **Alternativas** (se houver 1-2 opções viáveis)

### 5. Perguntar ao Usuário

Usar `AskUserQuestion` para confirmar a sugestão:

- header: "Próxima tarefa"
- question: "Concorda com a próxima tarefa sugerida?"
- options:
  - Sim, criar Issue (Criar Issue com a tarefa sugerida)
  - Escolher alternativa (Se houver alternativas listadas, escolher uma)
  - Outra tarefa (Descrever manualmente a tarefa desejada)

### 6. Criar Issue via `/pdir-criar-issue`

**Se o usuário concordou** → executar `/pdir-criar-issue [título sugerido]`

**Se escolheu alternativa** → executar `/pdir-criar-issue [título da alternativa escolhida]`

**Se indicou outra tarefa** → executar `/pdir-criar-issue [descrição fornecida pelo usuário]`

O `/pdir-criar-issue` cuidará de toda a lógica de labels, milestone e criação da Issue.

### 7. Feedback Final

```
Próxima tarefa registrada!

[Saída do /pdir-criar-issue]

Próximos passos:
- Execute /clear para limpar o contexto
- /pdir-implementar-tarefa [número-da-issue] (na próxima sessão)

Dica: este comando também está disponível como alternativa contextual ao /pdir-criar-issue.
```
