---
description: Divide plano em grupos e subgrupos (estrutura hierárquica)
argument-hint: [arquivo-plano] [grupos|subgrupos]
---

# PDIR: Listar Grupos

Analisa um plano e cria estrutura hierárquica organizando em grupos lógicos **SEM numeração**.

**Exemplos de uso pelo usuário**:

```bash
/pdir-listar-grupos arquivo-de-PRD #(subgrupos por default)
/pdir-listar-grupos @plano-auth.md grupos
/pdir-listar-grupos "Sistema de notificações com email, SMS e push" grupos
```

## Argumentos

- `$1`: Plano (arquivo com `@` ou texto direto) - obrigatório
- `$2`: `grupos` (1 nível) ou `subgrupos` (2 níveis) - padrão, se ausente: `subgrupos`

## Instruções

### Criar Pasta (se não existir)

```bash
mkdir -p docs/projeto/grupos
```

### Processar Input

- Se começa com `@` ou termina em `.md`: ler arquivo
- Caso contrário: usar como texto direto
- `$2 = "grupos"`: 1 nível | `$2 = "subgrupos"` ou ausente: 2 níveis

### Escolher Classificação

Analise o plano e escolha o modelo mais adequado:

| Tipo de Conteúdo | Classificação | Exemplo |
|------------------|---------------|---------|
| Áreas funcionais | Domínios → Subdomínios | Autenticação → Login, Registro |
| Features grandes | Épicos → Features | Onboarding → Tutorial, Perfil |
| Arquitetura modular | Módulos → Componentes | API → Endpoints, Middlewares |
| Implementação sequencial | Fases → Etapas | Setup → Infraestrutura, Config |
| Camadas | Camadas → Áreas | Backend → Database, API |

### Gerar Arquivo

**Saída:** `docs/projeto/grupos/lista-grupos-[plano-referenciado].md`

**Cabeçalho:**
```markdown
# [Classificação] - [Nome do Plano]

> **Baseado em:** [arquivo ou "plano fornecido"]
> **Nível:** [Grupos | Grupos e Subgrupos]
> **Modelo:** [tipo de classificação]
> **Data:** YYYY-MM-DD
```

### Criar Estrutura (após o cabeçalho)

#### Formato (1 nível):

```markdown
## Nome do primeiro Grupo

Descrição (1-2 linhas).

## Nome do segundo Grupo

Descrição (1-2 linhas).

## Nome do terceiro Grupo

Descrição (1-2 linhas).
```

#### Formato (2 níveis):

```markdown
## Nome do primeiro Grupo

Descrição (1-2 linhas).

### Nome do primeiro Subgrupo do primeiro Grupo

Descrição (1 linha).

## Nome do segundo Grupo

Descrição (1-2 linhas).

### Nome do primeiro Subgrupo do segundo Grupo

Descrição (1 linha).

### Nome do segundo Subgrupo do segundo Grupo

Descrição (1 linha).
... ...

```
### Regras

- Não numerar: "Grupo 1", "Subgrupo 1.1"
- Nomes descritivos: "Autenticação", "Login e Sessão"
- Descrições breves e objetivas
- Não incluir tarefas

### Feedback Final

```
Estrutura criada!

Arquivo: docs/projeto/grupos/lista-grupos-[nome].md
Grupos: [N] | Subgrupos: [N]

Próximo passo: /pdir-listar-tarefas "Nome do Grupo"
```
