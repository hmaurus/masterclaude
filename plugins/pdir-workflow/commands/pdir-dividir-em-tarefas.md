---
description: Divide plano ou funcionalidade em tarefas atômicas
argument-hint: [arquivo-ou-texto] [seção-opcional]
---

# PDIR: Dividir em Tarefas

Divide um plano, fase ou funcionalidade em tarefas atômicas de implementação.

**Exemplos de uso pelo usuário**:

```bash
# PRD completo
/pdir-dividir-em-tarefas @docs/projeto/PRD.md

# Fase específica do PRD
/pdir-dividir-em-tarefas @docs/projeto/PRD.md "Fase 1 - Fundação"

# Plano de uma funcionalidade
/pdir-dividir-em-tarefas @docs/projeto/plano-auth.md

# Texto direto
/pdir-dividir-em-tarefas "Sistema de notificações com email e SMS"
```

## Argumentos
- `$1`: Arquivo (com `@`) ou texto direto - **obrigatório**
- `$2`: Título da seção/fase dentro do arquivo (quando `$1` é arquivo) - **opcional**

## Instruções

### Criar Pasta (se não existir)

```bash
mkdir -p docs/projeto/tarefas
```

### Processar Input

**Se `$1` é arquivo E `$2` fornecido:**
- Ler arquivo `$1`
- Buscar seção com título `$2` (ex: "Fase 1 - Fundação")
- Extrair conteúdo dessa seção específica
- Usar como escopo para criar tarefas

**Se `$1` é arquivo (sem `$2`):**
- Ler arquivo completo
- Usar como escopo

**Se `$1` é texto:**
- Usar como texto direto descrevendo o escopo

### Dividir em Tarefas

Para divisão, imagine os seguintes critérios de tamanho e complexidade que cada Tarefa terá após implementada:

| Critério | Medida |
|----------|--------|
| Arquivos | 1-3 arquivos |
| Linhas de código | ~50-400 linhas |
| Objetivo | 1 objetivo claro |
| Dependências | ≤3 outras tarefas |
| Testabilidade | Isoladamente |

**Boas práticas:**
- Atômica: uma mudança lógica
- Específica: escopo bem definido
- Testável: sabe quando está pronta
- Independente: mínimas dependências

### Criar Títulos

**Formato:** `[type](domain): descrição curta e clara`

**Types:**

`feat`, `fix`, `refactor`, `docs`, `test`, `chore` ...

**Domain:** Termos do projeto (`auth`, `api`, `ui`, `db`, `user`, `posts`, `payments`)

### Gerar Arquivo

**Saída:** `docs/projeto/tarefas/lista-tarefas-[plano-ou-grupo-do-input].md`

**Estrutura:**

```markdown
# Tarefas - [Nome do Escopo]

> **Baseado em:** [origem]
> **Data:** YYYY-MM-DD
> **Total:** [número] tarefas

## Ordem de Implementação

As tarefas estão em ordem lógica. Tarefas com `Depende de` aguardam conclusão das dependências.

---

## [type](domain): título da primeira tarefa

**Descrição:** O que deve ser feito (1-3 linhas).

**Arquivos estimados:** [número] arquivo(s)

**Dependências:** Nenhuma (ou Depende de: #[números])

---

## [type](domain): título da segunda tarefa ...
```

### Instruções para Ordem de Implementação

**Ordem típica:**
1. Setup/Infraestrutura (schema, config)
2. Modelos/Types
3. Utilitários/Helpers
4. Lógica de negócio
5. API/Endpoints
6. UI/Frontend
7. Testes
8. Documentação

**Dependências:**
- Tarefas sem dependências primeiro
- Marque explicitamente com `Depende de: #[números]`

## Dicas

**Faça:**
- Tarefas atômicas e autocontidas
- Verbos de ação claros (implementar, criar, adicionar, corrigir)
- Escopo pequeno (1 PR, 1 review)
- Identifique dependências explicitamente

**Evite:**
- Tarefas muito grandes (>500 linhas)
- Tarefas vagas ("melhorar código")
- Múltiplos objetivos em uma tarefa
- Muitos arquivos (>5)

**Divisão correta:**

Grande: `feat(posts): implementar sistema completo`

Dividida:
- `feat(posts): criar schema e model`
- `feat(posts): criar endpoint POST /api/posts`
- `feat(posts): criar endpoint GET /api/posts`
- `feat(posts): criar página de listagem`
- `feat(posts): adicionar paginação`

### Feedback Final

```
Lista de tarefas criada!

Arquivo: docs/projeto/tarefas/lista-tarefas-[nome].md
Total: [N] tarefas

Próximo passo: /pdir-criar-issue "título da tarefa"
```
