---
description: Divide PRD ou outro documento em tarefas atômicas
argument-hint: <arquivo>#<seção> [/skill1 /skill2 ...] | <descrição livre> [/skill1 /skill2 ...]
---

# PDIR: Dividir em Tarefas

Divide um documento ou descrição em tarefas atômicas para implementação por AI Code Assistants.

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Skills:** palavras começando com `/` (ex: `/brainstorming /feature-dev`). Se passadas, carregá-las **obrigatoriamente** antes de prosseguir.
- **Restante:** referência a documento ou descrição livre.

## Formato

```bash
/pdir-dividir-em-tarefas docs/projeto/PRD.md#Fase 1 - Fundação
/pdir-dividir-em-tarefas docs/projeto/PRD.md /brainstorming
/pdir-dividir-em-tarefas Sistema de notificações com email e SMS
```

## Instruções

### 1. Identificar Escopo

**Se contém `#`** → ler arquivo, buscar seção que contenha o trecho após `#`, extrair conteúdo dessa seção como escopo.

**Se contém nome de arquivo (sem `#`)** → ler arquivo completo como escopo.

**Caso contrário** → usar como descrição livre.

### 2. Dividir em Tarefas

Cada tarefa deve ser:
- **Atômica:** uma mudança lógica, escopo de 1 PR
- **Específica:** verbos de ação claros (implementar, criar, adicionar, corrigir)
- **Testável:** critérios claros de conclusão
- **Independente:** mínimas dependências entre tarefas

Ordenar por dependência: infra/config → modelos/types → lógica de negócio → API → UI → testes.

### 3. Gerar Arquivo

Criar `docs/projeto/tarefas/` se não existir.

**Saída:** `docs/projeto/tarefas/lista-tarefas-[nome-do-escopo].md`

```markdown
# Tarefas - [Nome do Escopo]

> **Baseado em:** [origem]
> **Data:** YYYY-MM-DD
> **Total:** [número] tarefas

---

## type(scope): título da tarefa

**Descrição:** O que deve ser feito

**Arquivos estimados:** [número] arquivo(s)

**Dependências:** Nenhuma (ou Depende de: títulos das tarefas)

---
```

**Títulos:** formato `type(scope): descrição curta`. Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`. Scope: área do projeto inferida do contexto.

### 4. Feedback Final

```
Lista de tarefas criada!

Arquivo: docs/projeto/tarefas/lista-tarefas-[nome].md
Total: [N] tarefas

Próximos passos:
- /pdir-criar-issue docs/projeto/tarefas/lista-tarefas-[nome].md#título da tarefa
```
