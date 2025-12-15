# Masterclaude - Guidelines de Desenvolvimento

Marketplace de plugins para Claude Code.

## Estrutura

```
masterclaude/
├── .claude-plugin/
│   └── marketplace.json    # Lista de plugins do marketplace
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json # Manifest do plugin (versão aqui)
│       ├── commands/       # Comandos do plugin
│       ├── agents/         # Agentes (opcional)
│       └── skills/         # Skills (opcional)
└── CLAUDE.md
```

## Versionamento

- **Semver**: MAJOR.MINOR.PATCH
- **Fonte da verdade**: `plugins/<plugin>/.claude-plugin/plugin.json`
- **Quando incrementar**:
  - PATCH (0.0.X): correções de bugs
  - MINOR (0.X.0): novas funcionalidades compatíveis
  - MAJOR (X.0.0): mudanças incompatíveis

## Workflow de Desenvolvimento

1. Fazer alterações no plugin
2. Atualizar versão em `plugins/<plugin>/.claude-plugin/plugin.json`
3. Commit e push
4. Usuários atualizam via `/plugin` → "Update now"

## Comandos em Plugins

- Evitar operadores shell compostos (`||`, `&&`, `;`) em comandos inline `!`comando``
- Deixar lógica condicional em texto (Claude interpreta naturalmente)
- Comandos simples são mais compatíveis com CLI e extensão VS Code

## Para Usuários

```bash
# Adicionar marketplace
/plugin marketplace add masterclaude https://github.com/hmaurus/masterclaude

# Instalar plugin
/plugin install pdir-workflow@masterclaude

# Atualizar
/plugin  # Navegar até o plugin → "Update now"
```
