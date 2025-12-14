# MasterClaude

Marketplace de plugins Claude Code por Maurus Henriques.

## Instalação

```bash
# Adicionar o marketplace
/plugin marketplace add hmaurus/masterclaude
```

## Plugins Disponíveis

### pdir-workflow

Método PDIR (Planejar, Dividir, Implementar, Revisar) para desenvolvimento estruturado com IA.

```bash
/plugin install pdir-workflow@hmaurus-masterclaude
```

#### Pré-requisitos

- **GitHub CLI** (`gh`) autenticado: `gh auth login`
- **Git** configurado com acesso ao repositório

#### Comandos

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

#### Fluxo

```
PRD.md → Grupos → Tarefas → Issue → Implementar → Commit → PR → Merge
```

## Estrutura

```
masterclaude/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── pdir-workflow/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── commands/
│           └── *.md
└── README.md
```

## Troubleshooting

### Comandos não aparecem

```bash
/plugin uninstall pdir-workflow@hmaurus-masterclaude
/plugin install pdir-workflow@hmaurus-masterclaude
```

### Erro "gh: command not found"

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Autenticar
gh auth login
```

## Licença

MIT

---

**Autor:** Maurus Henriques - maurus@maurus.com.br
