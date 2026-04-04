# pdir-workflow

Plugin de comandos composáveis para o **Método JIT** — desenvolvimento estruturado com IA usando planejamento just-in-time.

## Pré-requisitos

- [GitHub CLI (`gh`)](https://cli.github.com/) instalado e autenticado
- Git configurado

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/pdir-criar-prd` | Cria PRD (roadmap com checklist de demandas) via entrevista |
| `/pdir-criar-spec` | Cria spec via entrevista em profundidade (Interview Pattern) |
| `/pdir-proxima-demanda` | Sugere próxima demanda do PRD |
| `/pdir-validar-implementacao` | Valida contra a spec, documenta na Issue e atualiza PRD |
| `/pdir-commit` | Commit e push com Conventional Commits |
| `/pdir-criar-pr` | Cria PR com validação antes |
| `/pdir-merge-pr` | Squash merge + limpeza de branch |
| `/pdir-deploy` | Merge para produção |

## Fluxo Típico

```
/pdir-criar-prd                  → PRD do projeto via entrevista (1x no início)
/pdir-proxima-demanda            → escolher próxima demanda do PRD
/pdir-criar-spec "demanda X"     → spec da demanda via entrevista
/clear
"Implemente a spec em docs/projeto/specs/spec-X.md"  → plan-mode nativo
/pdir-validar-implementacao docs/projeto/specs/spec-X.md
/pdir-commit
/pdir-criar-pr
/pdir-merge-pr
/pdir-deploy
```

Demandas simples não precisam de spec — vão direto para plan-mode.

## Método JIT

Este plugin implementa ferramentas composáveis para o [Método JIT](https://aicodingflow.com), uma metodologia onde:

- O **humano** define o quê (PRD, demandas, specs)
- O **AI** planeja e executa o como (plan-mode, implementação)
- Cada comando é **independente** — use conforme a necessidade, não por obrigação de pipeline

## Licença

MIT
