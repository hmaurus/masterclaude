---
description: Analisa contexto atual e projeto para sugerir a próxima demanda a implementar. Ideal para usar após concluir uma demanda, antes do /clear
argument-hint: [arquivo-prd]
---

# PDIR: Próxima Demanda

Analisa o contexto da sessão atual, o plano do projeto e as Issues do GitHub para sugerir a próxima demanda a implementar. Ideal para ser executado logo após concluir uma demanda, aproveitando o contexto fresco antes do `/clear`.

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

`$ARGUMENTS` (opcional): caminho para PRD. Se não fornecido, usar `docs/projeto/PRD.md` como padrão.

## Instruções

### 1. Analisar Contexto da Sessão Atual

Resumir brevemente o que foi feito nesta sessão:
- Qual demanda foi implementada
- Quais arquivos foram criados ou modificados
- Qual área do projeto foi alterada (ex: auth, API, UI, infra)

### 2. Buscar Plano do Projeto

**Se `$ARGUMENTS` fornecido** → usar como caminho do documento.

**Se não** → usar `docs/projeto/PRD.md`.

Se o arquivo existir, ler e identificar:
- Demandas já concluídas (marcadas com `[x]` ou similar)
- Demandas pendentes (`- [ ]`)
- Ordem de prioridade/dependência

Se o arquivo não existir, pular para o passo 3.

### 3. Verificar Specs e Issues

```bash
# Specs existentes
ls docs/projeto/specs/ 2>/dev/null

# Issues abertas
gh issue list --state open --limit 30 --json number,title,labels

# Issues fechadas recentemente
gh issue list --state closed --limit 10 --json number,title
```

Identificar:
- Specs pendentes (sem sufixo `_concluida`)
- Specs concluídas (com sufixo `_concluida`)
- Issues abertas sem spec correspondente

### 4. Sugerir Próxima Demanda

Considerar:
- **Dependências:** o que a demanda recém-implementada desbloqueou
- **Ordem lógica:** seguir a sequência do PRD
- **Specs pendentes:** priorizar demandas que já têm spec escrita
- **Prioridade natural:** infra/config → modelos/types → lógica → API → UI

Apresentar a sugestão com:
- **Título** descritivo
- **Justificativa** breve de por que esta é a próxima demanda lógica
- **Alternativas** (se houver 1-2 opções viáveis)

### 5. Feedback Final

```
Próxima demanda sugerida!

Sugestão: [título]
Justificativa: [breve]
Alternativas: [se houver]

Próximos passos:
- /clear
- /pdir-criar-spec [título] (na próxima sessão)
```
