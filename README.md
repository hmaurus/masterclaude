# MasterClaude

Marketplace de plugins Claude Code por Maurus Henriques.

## Instalação

```bash
# Adicionar o marketplace
/plugin marketplace add hmaurus/masterclaude
```

## Plugins Disponíveis

### pdir-workflow

Comandos composáveis para o **Método JIT** — desenvolvimento estruturado com IA usando planejamento just-in-time.

```bash
/plugin install pdir-workflow@hmaurus-masterclaude
```

#### Pré-requisitos

- **GitHub CLI** (`gh`) autenticado: `gh auth login`
- **Git** configurado com acesso ao repositório

#### Comandos

| Comando | Descrição |
|---------|-----------|
| `/pdir-criar-spec` | spec via entrevista em profundidade |
| `/pdir-validar-implementacao` | valida + documenta + atualiza PRD |
| `/pdir-commit` | commit + push |
| `/pdir-criar-pr` | cria PR com validação antes |
| `/pdir-merge-pr` | squash merge + limpeza |
| `/pdir-deploy` | merge para produção |
| `/pdir-proxima-demanda` | sugere próxima demanda |

#### Fluxo

```
Spec → /clear → Plan-mode → Validar → Commit → PR → Merge → Deploy
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
