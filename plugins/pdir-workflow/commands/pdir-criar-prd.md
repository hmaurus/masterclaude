---
description: Cria PRD (Product Requirements Document) do projeto
argument-hint: [descrição do projeto]
---

# PDIR: Criar PRD

Gera um documento de requisitos do produto baseado em entrevista ao usuário usando AskUserQuestion.

**Exemplos de uso:**

```bash
/pdir-criar-prd "App de delivery de comida para restaurantes locais"
/pdir-criar-prd  # (interativo - pergunta descrição)
```

## Argumentos

- `$ARGUMENTS`: Descrição, plano ou ideia inicial do projeto (opcional - se ausente, perguntar)

## Instruções

### 1. Criar Pasta (se não existir)

```bash
mkdir -p docs/projeto
```

### 2. Gerar PRD

Criar `docs/projeto/PRD.md` usando o template abaixo.

**Diretrizes:**
- Tom profissional e direto
- Foco em MVP (3-7 funcionalidades)
- Inferências razoáveis apenas
- Documento enxuto (1-2 páginas)

### Template PRD

```markdown
# PRD - [NOME_PROJETO]

## Visão Geral

[DESCRIÇÃO expandida - 2-3 parágrafos]

## Objetivo do MVP

[Objetivo claro e mensurável]

## Público-Alvo

[Público principal e secundário]

## Funcionalidades do MVP

### Fase 1 - [Nome descritivo]
- **[Funcionalidade]** - Descrição breve | Valor entregue
- **[Funcionalidade]** - Descrição breve | Valor entregue

### Fase 2 - [Nome descritivo]
- **[Funcionalidade]** - Descrição breve | Valor entregue
- **[Funcionalidade]** - Descrição breve | Valor entregue

### Fase 3 - [Nome descritivo]
- **[Funcionalidade]** - Descrição breve | Valor entregue

[3-7 funcionalidades no total, organizadas em 2-4 fases por ordem de implementação]

## Requisitos Não-Funcionais

- Performance: < 3s carregamento
- Segurança: validação de inputs, autenticação
- Acessibilidade: WCAG AA
- Responsivo (caso seja web): mobile-first

## Próximos Passos

1. Revisar e ajustar este PRD
2. `/pdir-dividir-em-tarefas @docs/projeto/PRD.md "Fase 1 - [nome]"`

---

*PRD gerado automaticamente. Revise antes de prosseguir.*
```

### Feedback Final

```
✅ PRD criado!

📄 Arquivo: docs/projeto/PRD.md

Próximos passos:
1. Revisar o PRD gerado
2. /pdir-dividir-em-tarefas @docs/projeto/PRD.md "Fase 1 - [nome]"
```

**Dica:** Para refinamento colaborativo do PRD, considere usar `/doc-coauthoring` ou outras skills de documentação disponíveis.
