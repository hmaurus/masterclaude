---
description: Cria lista de tarefas a partir de plano/grupo/subgrupo
argument-hint: [lista-grupos-ou-titulo-do-grupo-subgrupo] [titulo-grupo-ou-subgrupo-contido-no-primeiro-argumento]
---

# PDIR: Listar Tarefas

Gera um arquivo markdown com lista de tarefas de um grupo ou subgrupo específico ou direto de um plano dependendo do input.

**Exemplos de uso pelo usuário**:

```bash
# Plano de uma funcionalidade
/pdir-listar-tarefas @docs/projeto/plano-auth.md

# Lista de grupos + título do grupo/subgrupo
/pdir-listar-tarefas @docs/projeto/lista-grupos-PRD.md "Autenticação e Autorização"
/pdir-listar-tarefas @docs/projeto/lista-grupos-PRD.md "Login e Sessão"

# Nome de grupo apenas (sem contexto da lista de grupos)
/pdir-listar-tarefas "Autenticação e Autorização"

# Texto direto
/pdir-listar-tarefas "Sistema de notificações com email e SMS"
```

## Argumentos
- `$1`: Arquivo (com `@`), nome de grupo/subgrupo, ou texto direto - **obrigatório**
- `$2`: Título do grupo/subgrupo (quando `$1` é arquivo de lista de grupos) - **opcional**

## Instruções

### Criar Pasta (se não existir)

```bash
mkdir -p docs/projeto/tarefas
```

### Processar Input

**Se `$1` é arquivo de lista de grupos (`lista-grupos-*.md`) E `$2` fornecido:**
- Ler arquivo `$1`
- Buscar seção com título `$2` (grupo ou subgrupo)
- Extrair conteúdo dessa seção específica
- Usar como escopo para criar tarefas

**Se `$1` é arquivo (plano, não lista de grupos):**
- Ler arquivo completo
- Usar como escopo

**Se `$1` é texto:**
- Se parece ser nome de grupo: buscar em `docs/projeto/grupos/lista-grupos-*.md`
- Caso contrário: usar como texto direto

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
