# pdir-workflow

Método **PDIR** (Planejar, Dividir, Implementar, Revisar) para desenvolvimento estruturado com IA.

## Pré-requisitos

- [GitHub CLI (`gh`)](https://cli.github.com/) instalado e autenticado
- Git configurado

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/pdir-dividir-em-tarefas` | Divide PRD ou documento em tarefas atômicas |
| `/pdir-criar-issue` | Cria Issue no GitHub a partir de tarefas ou descrição livre |
| `/pdir-implementar-tarefa` | Implementa tarefa a partir de Issue existente |
| `/pdir-commit` | Commit e push com Conventional Commits |
| `/pdir-criar-pr` | Cria Pull Request vinculado a Issue |
| `/pdir-merge-tarefa` | Valida, faz merge e limpa branch |

## Fluxo Típico

```
Planejar PRD → Dividir em Tarefas → Criar Issues → Implementar → Commit → PR → Merge
```

## Criar um PRD

Este plugin foca no ciclo a partir da divisão em tarefas. Para criar um PRD (`docs/projeto/PRD.md`), use uma dessas abordagens:

- **`/doc-coauthoring`** — co-autoria interativa com entrevista, refinamento e teste de clareza (requer skill `doc-coauthoring`)
- **`/brainstorming`** — exploração criativa de requisitos antes de estruturar o PRD
- **Conversa direta** — descreva o projeto ao Claude e peça para criar o PRD em `docs/projeto/PRD.md`

Após ter o PRD, inicie o fluxo com `/pdir-dividir-em-tarefas docs/projeto/PRD.md`.

## Licença

MIT
