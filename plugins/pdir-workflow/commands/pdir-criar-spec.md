---
description: Cria documento de especificação (spec) via entrevista em profundidade sobre a demanda. Gera input ideal para plan-mode
argument-hint: "<descrição breve da demanda>"
---

# PDIR: Criar Spec

Cria um documento de especificação completo a partir de uma entrevista em profundidade com o usuário. Baseado no Interview Pattern documentado pela Anthropic.

**Este comando NÃO planeja nem implementa. Ele produz apenas a spec — o input ideal para o plan-mode do Claude Code.**

**Em qualquer passo, se algo falhar ou faltar informação, informe o erro e pergunte ao usuário como prosseguir.**

## Processar $ARGUMENTS

Extrair do `$ARGUMENTS`:
- **Descrição da demanda:** o que o usuário quer construir

Se vazio: perguntar ao usuário o que ele quer construir.

## Instruções

### 1. Explorar Contexto do Projeto

Ler CLAUDE.md, README.md e arquivos relacionados à demanda. Entender stack, padrões e estrutura existentes para fazer perguntas informadas.

### 2. Entrevistar o Usuário

Entrevistar o usuário em profundidade usando AskUserQuestion. Cobrir:
- Implementação técnica
- UI/UX
- Edge cases
- Preocupações
- Tradeoffs

Regras da entrevista:
- **Não perguntar o óbvio** — focar nas partes difíceis que o usuário pode não ter considerado
- **Ir fundo** — se uma resposta revela complexidade, explorar antes de avançar
- **Continuar até cobrir tudo** — não encerrar prematuramente

### 3. Gerar Spec

Criar `docs/projeto/specs/` se não existir.

**Saída:** `docs/projeto/specs/spec-[nome-da-demanda].md`

Escrever uma spec completa cobrindo tudo que foi discutido na entrevista. Formato livre — estruturar conforme fizer sentido para a demanda, sem template rígido.

### 4. Revisar com o Usuário

Apresentar a spec e perguntar se algo está faltando, errado ou ambíguo. Ajustar até o usuário aprovar.

### 5. Feedback Final

```
Spec criada!

Arquivo: docs/projeto/specs/spec-[nome].md

Próximos passos:
1. /clear — limpar contexto antes de implementar
2. Entrar em plan-mode e pedir para implementar a spec:
   "Planeje e implemente a spec em docs/projeto/specs/spec-[nome].md"
```
