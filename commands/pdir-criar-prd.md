---
description: Cria PRD (Product Requirements Document) do projeto
argument-hint: [descrição do projeto]
---

# PDIR: Criar PRD

Gera um documento de requisitos do produto baseado na descrição fornecida.

**Exemplos de uso:**

```bash
/pdir-criar-prd "App de delivery de comida para restaurantes locais"
/pdir-criar-prd  # (interativo - pergunta descrição)
```

## Argumentos

- `$ARGUMENTS`: Descrição do projeto (opcional - se ausente, perguntar)

## Instruções

### 1. Coletar Descrição

**Se `$ARGUMENTS` vazio:** Usar `AskUserQuestion` para coletar:
- Nome do projeto
- Descrição (objetivo, público-alvo, funcionalidades principais)

**Se `$ARGUMENTS` fornecido:** Usar como descrição.

### 2. Criar Pasta (se não existir)

```bash
mkdir -p docs/projeto
```

### 3. Gerar PRD

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

## Principais Funcionalidades (MVP)

1. **[Funcionalidade 1]**
   - Descrição breve
   - Valor entregue

2. **[Funcionalidade 2]**
   - Descrição breve
   - Valor entregue

[3-7 funcionalidades no total]

## Escopo Inicial

- [Item dentro do MVP]

## Fora do Escopo

- [Item para versões futuras]

## Requisitos Não-Funcionais

- Performance: < 3s carregamento
- Segurança: validação de inputs, autenticação
- Acessibilidade: WCAG AA
- Responsivo: mobile-first

## Próximos Passos

1. Revisar e ajustar este PRD
2. `/pdir-listar-grupos PRD.md`
3. `/pdir-listar-tarefas` para cada grupo

---

*PRD gerado automaticamente. Revise antes de prosseguir.*
```

### Feedback Final

```
✅ PRD criado!

📄 Arquivo: docs/projeto/PRD.md

Próximos passos:
1. Revisar o PRD gerado
2. /pdir-listar-grupos PRD.md
```
