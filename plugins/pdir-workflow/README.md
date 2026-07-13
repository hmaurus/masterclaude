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
commit                           → "commit" em linguagem natural
/pdir-criar-pr
/pdir-merge-pr
/pdir-deploy
```

Demandas simples não precisam de spec — vão direto para plan-mode.

## Git: o que o Claude já faz vs. o que o PDIR agrega

Quando você diz "commit" (linguagem natural, sem comando), o Claude Code já faz sozinho: roda `git status`/`diff`/`log`, **segue o padrão de commit do repo**, faz stage só dos arquivos relacionados, **nunca usa `--amend`**, nunca roda comando destrutivo, não commita `.env` e só commita quando você pede. Por isso o PDIR não tem um comando de commit — seria andaime sobre o que já existe.

O que o comportamento nativo **não** cobre, e vale configurar, são duas regras. Cole no `CLAUDE.md` do seu projeto:

```markdown
## Git — convenção de commit

- **Conventional Commits com scope obrigatório:** `type(scope): descrição`.
  Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `style`, `test`, `perf`, `ci`, `build`.
- **Antes de `git push`:** se a branch tem upstream, rodar `git pull --ff-only`.
```

No ciclo PDIR o commit é linguagem natural; os passos com efeito colateral real (abrir PR, ir pra produção) continuam comandos explícitos, porque aí o timing na sua mão faz parte da segurança.

## Método JIT

Este plugin implementa ferramentas composáveis para o [Método JIT](https://aicodingflow.com), uma metodologia onde:

- O **humano** define o quê (PRD, demandas, specs)
- O **AI** planeja e executa o como (plan-mode, implementação)
- Cada comando é **independente** — use conforme a necessidade, não por obrigação de pipeline

## Licença

MIT
