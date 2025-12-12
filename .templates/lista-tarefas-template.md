# Tarefas - [Nome do Escopo]

> Baseado em: [caminho/arquivo-original.md ou descrição do escopo]
> Data: [YYYY-MM-DD]
> Total de tarefas: [número]

---

## Ordem de Implementação

As tarefas estão organizadas em ordem lógica de implementação. Tarefas marcadas com `⚠️ Depende de` devem aguardar a conclusão das dependências.

---

## [type](domain): título da tarefa

**Descrição:** Breve descrição do que deve ser feito (1-3 linhas). Foco no "o quê" e "por quê", não no "como".

**Arquivos estimados:** [número] arquivo(s)

**Dependências:** Nenhuma (ou ⚠️ Depende de: #[números das tarefas])

---

## [type](domain): título da segunda tarefa

**Descrição:** ...

**Arquivos estimados:** ...

**Dependências:** ...

---

## [type](domain): título da terceira tarefa

**Descrição:** ...

**Arquivos estimados:** ...

**Dependências:** ...

---

## Observações

### Critérios de Tamanho Ideal

Cada tarefa deve seguir:
- ✅ 1-3 arquivos modificados/criados
- ✅ Aproximadamente 50-400 linhas de código
- ✅ 1 objetivo funcional claro
- ✅ ≤3 dependências de outras tarefas
- ✅ Testável isoladamente

### Types Válidos

- `feat` - Nova funcionalidade
- `fix` - Correção de bug
- `refactor` - Refatoração de código
- `docs` - Documentação
- `test` - Adição/modificação de testes
- `chore` - Tarefas de manutenção
- `style` - Formatação, estilo
- `perf` - Melhoria de performance
- `build` - Build system, dependências
- `ci` - CI/CD

### Formato do Título

```
[type](domain): descrição curta e clara
```

**Exemplos:**
```
feat(auth): implementar login com email e senha
fix(api): corrigir erro 401 no refresh token
docs(cms): documentar fluxo de criação de posts
refactor(db): migrar queries para Prisma ORM
test(user): adicionar testes unitários para UserService
```