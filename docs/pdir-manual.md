# Método PDIR Workflow

O PDIR (Planejar, Dividir, Implementar, Revisar) é um método para desenvolver software de forma estruturada usando IA.

**Autor:** Maurus Henriques - maurus@maurus.com.br

---

## Visão Geral do Fluxo

```
PRD.md → Grupos → Tarefas → Issue → Implementar → Commit → PR → Merge
```

## Fase 1: Criar o PRD

O PRD (Product Requirements Document) é o ponto de partida.

```bash
/pdir-criar-prd "Descrição do seu projeto"
```

**Resultado:** `docs/projeto/PRD.md`

## Fase 2: Dividir o PRD em Grupos

```bash
/pdir-listar-grupos PRD.md subgrupos
```

**Resultado:** `docs/projeto/grupos/lista-grupos-PRD.md`

Estrutura hierárquica com grupos e subgrupos. Exemplo:

```markdown
## Grupo: Autenticação
### Subgrupo: Login
### Subgrupo: Registro
### Subgrupo: Recuperação de Senha

## Grupo: Dashboard
### Subgrupo: Visão Geral
### Subgrupo: Relatórios
```

**Dica:** Use `grupos` em vez de `subgrupos` para projetos menores.

## Fase 3: Gerar Tarefas por Grupo/Subgrupo

Para **cada** grupo ou subgrupo, execute:

```bash
/pdir-listar-tarefas grupos/lista-grupos-PRD.md "Subgrupo: Login"
```

**Resultado:** `docs/projeto/tarefas/lista-tarefas-login.md`

Lista de tarefas atômicas no formato `tipo(escopo): descrição`. Exemplo:

```markdown
- feat(auth): criar página de login
- feat(auth): implementar validação de credenciais
- feat(auth): adicionar autenticação com OAuth
- test(auth): testes unitários do login
```

**Repita** para cada grupo/subgrupo até ter todas as tarefas.

## Fase 4: Implementar Tarefas (Ciclo)

Para **cada** tarefa da lista:

### 4.1. Criar Issue

```bash
/pdir-criar-issue feat(auth): criar página de login
```

### 4.2. Implementar

```bash
/pdir-implementar-tarefa 42
```

Cria branch `feat/42-criar-pagina-login` e implementa a funcionalidade.

### 4.3. Commitar

```bash
/pdir-commit
```

Pode executar múltiplas vezes durante a implementação (commits incrementais).

### 4.4. Criar Draft PR

```bash
/pdir-draft-pr
```

### 4.5. Continuar Desenvolvimento (opcional)

```bash
/pdir-commit  # mais commits se necessário
```

### 4.6. Marcar Pronto e Fazer Merge

```bash
/pdir-ready-pr
/pdir-merge-tarefa
```

**Resultado:** PR merged, branch deletada, Issue fechada.

---

## Resumo dos Comandos

| Fase | Comando | O que faz |
|------|---------|-----------|
| PRD | `/pdir-criar-prd` | descrição → PRD.md |
| Dividir | `/pdir-listar-grupos` | PRD → grupos/subgrupos |
| Tarefas | `/pdir-listar-tarefas` | grupo → lista de tarefas |
| Issue | `/pdir-criar-issue` | tarefa → Issue GitHub |
| Implementar | `/pdir-implementar-tarefa` | Issue → branch + código |
| Commit | `/pdir-commit` | commit + push |
| PR | `/pdir-draft-pr` | cria Draft PR |
| Ready | `/pdir-ready-pr` | marca PR pronto |
| Merge | `/pdir-merge-tarefa` | merge + limpeza |

---

## Fluxo Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    /pdir-criar-prd                          │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        PRD.md                               │
└─────────────────────────┬───────────────────────────────────┘
                          │ /pdir-listar-grupos
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              lista-grupos-PRD.md                            │
│  ├── Grupo: Auth                                            │
│  │   ├── Subgrupo: Login                                    │
│  │   └── Subgrupo: Registro                                 │
│  └── Grupo: Dashboard                                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ /pdir-listar-tarefas (por subgrupo)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              lista-tarefas-login.md                         │
│  - feat(auth): criar página de login                        │
│  - feat(auth): validar credenciais                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ Para cada tarefa:
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  /pdir-criar-issue                                          │
│  /pdir-implementar-tarefa [issue]                           │
│  /pdir-commit (1 ou mais vezes)                             │
│  /pdir-draft-pr                                             │
│  /pdir-commit (opcional)                                    │
│  /pdir-ready-pr                                             │
│  /pdir-merge-tarefa                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Dicas

- **Granularidade:** Uma tarefa = uma funcionalidade testável isoladamente
- **Commits:** Commite frequentemente, não espere terminar tudo
- **PRD primeiro:** Invista tempo no PRD antes de começar a dividir
- **Sequência:** Respeite dependências entre tarefas ao implementar

---

## Estrutura de Arquivos Gerada

```
seu-projeto/
├── docs/projeto/
│   ├── PRD.md                    # Plano geral do projeto
│   ├── grupos/                   # Arquivos de grupos (gerados)
│   │   └── lista-grupos-PRD.md
│   └── tarefas/                  # Arquivos de tarefas (gerados)
│       ├── lista-tarefas-login.md
│       └── lista-tarefas-registro.md
```

---

**Desenvolvido com Claude Code**
