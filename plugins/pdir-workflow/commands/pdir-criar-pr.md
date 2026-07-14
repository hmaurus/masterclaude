---
description: Cria Pull Request vinculado a uma Issue do GitHub. Extrai a Issue da branch automaticamente ou recebe o número explícito
argument-hint: [número-da-issue]
---

# PDIR: Criar PR

Cria um Pull Request vinculado a uma Issue, validando antes e padronizando o corpo.

**Pré-requisitos:** estar numa branch de feature (não no branch default) com os commits já feitos.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Descobrir a Issue

- **Com argumento** (`$ARGUMENTS`, ex: `42` ou `#42`): use os dígitos (descarte o `#`).
- **Sem argumento:** pegue o trecho entre a primeira `/` e o próximo `-` (ou o fim do nome, se não houver `-`). Use como número da Issue **somente se esse trecho for inteiramente dígitos**.
  - `feat/42-login` → trecho `42` → `#42` ✓
  - `feat/42` → trecho `42` → `#42` ✓
  - `feat/login-oauth2` → trecho `login` → pergunta
  - `feat/2fa-login` → trecho `2fa` → pergunta (não é só dígito)

**Não adivinhe.** Se o trecho não for inteiramente numérico, **não** pesque um dígito de dentro do slug — pergunte ao usuário qual é a Issue. Um número errado aqui vira `Closes #N` e fecha a Issue errada no merge.

## Instruções

### 1. Verificar estado

Descubra o branch default do repositório com `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` (não assuma `main` — pode ser `master`/`develop`); reuse esse valor nos passos seguintes.

Confirme, via git, que você **não** está no branch default e que não há mudanças não commitadas. Se estiver no default, encerre informando o motivo. Se houver pendências não commitadas, avise e sugira commitar primeiro (é só pedir "commit").

### 2. Validar

Rode os checks do projeto (lint, type-check, testes) — consulte `package.json`, `Makefile` ou equivalente para os comandos disponíveis. Se algum falhar, informe e pergunte se o usuário quer corrigir antes ou seguir mesmo assim. Validar **antes** do push evita disparar CI em código sabidamente quebrado.

### 3. Publicar a branch

Faça push da branch para o `origin`. Se ela ainda não tiver upstream, configure-o no push (`-u`); se já tiver, envie só os commits pendentes.

### 4. Confirmar a Issue e revisar o que mudou

- Leia a Issue (`gh issue view <número>`) e **mostre o título** — é a checagem de que você linkou a Issue certa. Se ela não existir, informe o número tentado e peça o correto. Se o número foi extraído da branch e o título não tiver relação com o trabalho da branch, confirme com o usuário antes de seguir.
- Reúna o contexto para o corpo do PR: os commits da branch (`git log <default>..HEAD --oneline`) e o resumo de arquivos **que o PR vai exibir**. Para o diff, use **três pontos** — `git diff <default>...HEAD --stat` —, que compara a partir do ponto de bifurcação (o que aparece na aba "Files changed"). Não use `git diff <default>` nem dois pontos: contra o tip atual do default, o resumo mistura mudanças que não são desta branch quando o default avançou.

### 5. Criar o PR

Antes de criar, cheque se já existe um PR aberto para essa branch. Se existir, mostre o link e pare — não abra outro.

Caso contrário, crie o PR contra o branch default. Derive:

- **título** no formato `tipo(escopo): descrição` — `tipo` do prefixo da branch, `escopo` da área principal dos arquivos modificados, descrição a partir da Issue;
- **corpo** exatamente com esta estrutura:

```markdown
Closes #<número-da-issue>

## Resumo

<resumo derivado da Issue e dos commits>

## Mudanças Principais

- <mudança 1>
- <mudança 2>
```

O `Closes #<número>` é obrigatório — é ele que amarra o PR à Issue e a fecha automaticamente no merge.

### 6. Feedback final

Informe ao usuário:

```
PR criado!

PR: #<número-do-pr>
Branch: <branch>
Link: <url>

Próximos passos:
- /pdir-merge-pr (quando aprovado)
- commit (se continuar desenvolvendo, é só pedir)
```
