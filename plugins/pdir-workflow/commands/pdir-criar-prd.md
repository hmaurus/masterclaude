---
description: Cria PRD (Product Requirements Document) via entrevista em profundidade sobre o projeto. Gera roadmap com checklist de demandas para o workflow PDIR
argument-hint: "<descrição breve do projeto>"
---

# PDIR: Criar PRD

Cria um PRD completo a partir de uma entrevista em profundidade com o usuário sobre o projeto. O PRD é o documento-raiz do workflow — define visão, escopo e o checklist de demandas consumido por `/pdir-proxima-demanda` e `/pdir-validar-implementacao`.

**Este comando NÃO cria specs nem implementa. Ele produz apenas o PRD — o roadmap do projeto.**

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Descrição do projeto:** o que o usuário quer construir

Se vazio: perguntar ao usuário qual projeto ele quer planejar.

## Instruções

### 1. Explorar Contexto Existente

Ler CLAUDE.md, README.md, `package.json` e arquivos relevantes. Se `docs/projeto/PRD.md` já existir, ler o conteúdo atual — pode ser uma atualização, não criação do zero.

Entender stack, estrutura e estado atual do projeto para fazer perguntas informadas.

### 2. Entrevistar o Usuário

Entrevistar o usuário em profundidade usando AskUserQuestion. Cobrir:

- **Visão e objetivo** — o que o projeto resolve, para quem
- **Escopo** — o que está dentro e fora do escopo
- **Funcionalidades** — listar todas as funcionalidades desejadas
- **Prioridades** — o que é essencial vs. desejável vs. futuro
- **Fases** — se faz sentido dividir em fases/milestones
- **Restrições** — prazos, tecnologias obrigatórias, limitações
- **Integrações** — APIs, serviços externos, dependências

Regras da entrevista:
- **Focar no macro** — escopo, prioridades, dependências entre funcionalidades
- **Não descer para detalhes de implementação** — isso é trabalho da spec
- **Ir fundo em prioridades** — se o usuário listar tudo como importante, desafiar para priorizar
- **Continuar até cobrir tudo** — não encerrar prematuramente

### 3. Gerar PRD

Criar `docs/projeto/` se não existir.

**Saída:** `docs/projeto/PRD.md`

Estrutura obrigatória do PRD:

```markdown
# PRD: [Nome do Projeto]

## Visão
[Descrição concisa do que o projeto é e resolve]

## Escopo
### Dentro do escopo
- ...

### Fora do escopo
- ...

## Stack / Restrições Técnicas
- ...

## Demandas

### Fase 1 — [nome da fase]
- [ ] Demanda 1 — descrição breve
- [ ] Demanda 2 — descrição breve

### Fase 2 — [nome da fase]
- [ ] Demanda 3 — descrição breve
- [ ] Demanda 4 — descrição breve

(quantas fases fizerem sentido)
```

Regras da saída:
- Cada demanda **deve** ser um item de checklist (`- [ ]`)
- Demandas devem ser granulares o suficiente para virar uma spec cada
- Ordenar por dependência dentro de cada fase (infra → modelos → lógica → API → UI)
- Se o projeto for simples, uma única fase sem título é suficiente

### 4. Revisar com o Usuário

Apresentar o PRD e perguntar se algo está faltando, errado ou mal priorizado. Ajustar até o usuário aprovar.

### 5. Feedback Final

```
PRD criado!

Arquivo: docs/projeto/PRD.md
Demandas: [N] total ([N] fase 1, [N] fase 2, ...)

Próximos passos:
1. /pdir-proxima-demanda — ver sugestão de primeira demanda
2. /pdir-criar-spec "[demanda]" — criar spec da demanda escolhida
```
