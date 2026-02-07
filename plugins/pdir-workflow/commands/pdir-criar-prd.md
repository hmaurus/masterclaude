---
description: Cria PRD (Product Requirements Document) do projeto
argument-hint: [descrição ou ideia inicial do projeto]
---

# PDIR: Criar PRD

Cria um PRD usando o skill `doc-coauthoring` para conduzir todo o processo de co-autoria.

## Argumentos

- `$ARGUMENTS`: Descrição ou ideia inicial do projeto (opcional — se ausente, o doc-coauthoring perguntará)

## Instruções

### 1. Criar pasta

Criar `docs/projeto/` se ainda não existir.

### 2. Acionar doc-coauthoring

Iniciar o workflow do skill `doc-coauthoring` com:

- **Arquivo de saída:** `docs/projeto/PRD.md`
- **Contexto inicial do usuário:** `$ARGUMENTS` (se fornecido)

O doc-coauthoring conduzirá:
1. Context Gathering (entrevista, info dump, perguntas clarificadoras)
2. Refinement & Structure (seção por seção, brainstorm, curadoria)
3. Reader Testing (teste com sub-agente fresh)

### 3. Feedback final

Após o doc-coauthoring concluir, exibir:

```
PRD criado!

Arquivo: docs/projeto/PRD.md

Próximos passos:
1. Revisar o PRD gerado
2. /pdir-dividir-em-tarefas @docs/projeto/PRD.md "Fase 1 - [nome]"
```
