---
description: Valida implementação contra a fonte da demanda (spec, Issue ou descrição). Roda CI, spec check e smoke test
argument-hint: "<número-issue | arquivo.md | descrição livre>"
---

# PDIR: Validar Implementação

Valida se a implementação atende à demanda original, documenta o que foi feito e atualiza o progresso do projeto. Pode ser usado após qualquer abordagem de implementação (plan-mode nativo, feature branch, correção manual).

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Fonte da demanda:** identificar o tipo:
  - **Número** (ex: `42`) → Issue do GitHub
  - **Caminho de arquivo** (ex: `docs/projeto/specs/spec-paywall.md`) → arquivo local
  - **Texto** → descrição livre

Se vazio: perguntar ao usuário qual a fonte da demanda.

## Instruções

### 1. Obter Escopo da Demanda

**Se Issue GitHub:**
```bash
gh issue view [número] --json number,title,body,comments
```
Analisar o body **e todos os comentários**.

**Se arquivo .md:** ler o arquivo completo.

**Se descrição livre:** usar o texto.

### 2. CI — Checks Automatizados

Consultar `package.json`, `Makefile` ou equivalente para identificar os comandos disponíveis. Executar:
- Lint
- Type-check
- Testes

Se algum check falhar, reportar no relatório mas continuar a validação.

### 3. Spec Check — Verificação contra o Escopo

Reler a fonte da demanda e verificar **item por item** se cada ponto foi atendido na implementação. Para cada item:
- Verificar se o código implementa o comportamento descrito
- Verificar se edge cases mencionados foram tratados

### 4. Smoke Test — Verificação Visual

Navegar pelas rotas afetadas pela implementação:
- Verificar se não há erros no console
- Verificar se o comportamento está correto visualmente
- Verificar se rotas existentes continuam funcionando

### 5. Relatório

```
Validação concluída!

Fonte: [#número - título | arquivo | descrição]

## CI
- Lint: [passou | falhou — detalhes]
- Type-check: [passou | falhou — detalhes]
- Testes: [passou | falhou — detalhes]

## Spec Check
- [item 1]: [atendido | não atendido — detalhes]
- [item 2]: [atendido | não atendido — detalhes]

## Smoke Test
- [rota 1]: [ok | erro — detalhes]
- [rota 2]: [ok | erro — detalhes]

## Resultado
[Tudo ok | Há itens pendentes — ver detalhes acima]
```

**Se houver falhas:** parar aqui. O usuário deve corrigir e rodar a validação novamente.

**Se tudo passou:** prosseguir para os passos 6 e 7.

### 6. Documentar na Issue (se aplicável)

**Apenas se a fonte foi uma Issue do GitHub:**

```bash
gh issue comment [número] --body "$(cat <<'EOF'
## Implementação Realizada

### Arquivos modificados/criados
- `arquivo.ts` - descrição

### Resumo
Breve descrição do que foi feito.
EOF
)"
```

Perguntar ao usuário se deseja fechar a issue agora.

### 7. Atualizar PRD

Verificar se existe `docs/projeto/PRD.md`. Se não existir, pular silenciosamente.

Se existir, ler o PRD e identificar no checklist (`- [ ]`, `- [x]`) o item que corresponde à demanda implementada. Se encontrar correspondência, perguntar ao usuário se deve marcar como concluído (`- [x]`).

### 8. Feedback Final

```
Validação e documentação concluídas!

Fonte: [#número - título | arquivo | descrição]
Issue: [comentada e fechada | comentada | N/A]
PRD: [item X marcado como concluído | sem alterações | não encontrado]

Próximos passos:
- /pdir-commit
- /pdir-criar-pr
```
