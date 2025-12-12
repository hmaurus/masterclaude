# PDIR Workflow Plugin

Plugin Claude Code para o método PDIR (Planejar, Dividir, Implementar, Revisar) - desenvolvimento estruturado com IA.

## Instalação

```bash
/plugin install hmaurus/pdir-workflow-plugin
```

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/pdir-criar-prd` | descrição → PRD.md |
| `/pdir-listar-grupos` | PRD → grupos/subgrupos |
| `/pdir-listar-tarefas` | grupo → lista de tarefas |
| `/pdir-criar-issue` | tarefa → Issue GitHub |
| `/pdir-implementar-tarefa` | Issue → branch + código |
| `/pdir-commit` | commit + push |
| `/pdir-draft-pr` | cria Draft PR |
| `/pdir-ready-pr` | marca PR pronto |
| `/pdir-merge-tarefa` | merge + limpeza |

## Fluxo PDIR

```
PRD.md → Grupos → Tarefas → Issue → Implementar → Commit → PR → Merge
```

### Fluxo Visual

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
└─────────────────────────┬───────────────────────────────────┘
                          │ /pdir-listar-tarefas (por grupo)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              lista-tarefas-[grupo].md                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ Para cada tarefa:
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  /pdir-criar-issue                                          │
│  /pdir-implementar-tarefa [issue]                           │
│  /pdir-commit (1 ou mais vezes)                             │
│  /pdir-draft-pr                                             │
│  /pdir-ready-pr                                             │
│  /pdir-merge-tarefa                                         │
└─────────────────────────────────────────────────────────────┘
```

## Pré-requisitos

- Claude Code CLI
- GitHub CLI (`gh`) autenticado
- Git configurado

## Estrutura

```
pdir-workflow-plugin/
├── .claude-plugin/plugin.json
├── .templates/
│   ├── PRD-template.md
│   ├── lista-grupos-template.md
│   └── lista-tarefas-template.md
├── commands/
│   ├── pdir-criar-prd.md
│   └── pdir/
│       ├── listar-grupos.md
│       ├── listar-tarefas.md
│       ├── criar-issue.md
│       ├── implementar-tarefa.md
│       ├── commit.md
│       ├── draft-pr.md
│       ├── ready-pr.md
│       └── merge-tarefa.md
└── docs/pdir-manual.md
```

## Documentação

Veja [docs/pdir-manual.md](docs/pdir-manual.md) para o manual completo.

## Licença

MIT

---

**Autor:** Maurus Henriques - maurus@maurus.com.br
