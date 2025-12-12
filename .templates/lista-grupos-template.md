# [Classificação Escolhida] - [Nome do Plano]

> **Baseado em:** [caminho/arquivo.md ou "plano fornecido"]
> **Nível:** [Grupos | Grupos e Subgrupos]
> **Modelo:** [Domínios/Subdomínios | Épicos/Features | Módulos/Componentes | Fases/Etapas | Camadas/Áreas]
> **Data:** [YYYY-MM-DD]

---

## [Nome do Grupo]

Breve descrição do que este grupo engloba (1-2 linhas).

### [Nome do Subgrupo] (opcional - apenas para nível "subgrupos")

Breve descrição deste subgrupo específico (1 linha).

### [Nome do Segundo Subgrupo] (opcional)

Breve descrição deste segundo subgrupo específico (1 linha).

---

## [Nome do Segundo Grupo]

...

### [Nome do Subgrupo] (opcional)

...

---

## Observações sobre o Template

### Modelos de Classificação Suportados

**1. Domínios e Subdomínios**
- Para sistemas com áreas funcionais distintas
- Exemplo: Autenticação → Login, Registro, OAuth

**2. Épicos e Features**
- Para produtos com funcionalidades de alto nível
- Exemplo: Onboarding → Tutorial, Perfil, Configurações

**3. Módulos e Componentes**
- Para arquiteturas modulares
- Exemplo: API Gateway → Roteamento, Segurança

**4. Fases e Etapas**
- Para projetos com implementação sequencial
- Exemplo: Setup Inicial → Infraestrutura, Dependências

**5. Camadas e Áreas**
- Para sistemas em camadas
- Exemplo: Backend → Database, Business Logic, API

### Regras Importantes

- ✅ **SEM numeração** em grupos e subgrupos
- ✅ Use nomes descritivos e semânticos do domínio
- ✅ Escolha modelo que melhor representa o plano
- ✅ Para nível "grupos": remova as seções de subgrupos
- ✅ Para nível "subgrupos": mantenha hierarquia completa
- ❌ NÃO use: "Grupo 1", "Subgrupo 1.1", "Parte A"
- ❌ NÃO detalhe tarefas (serão listadas em documentos separados)

### Critérios de Qualidade

**Grupos:**
- Coesos (áreas/domínios relacionados)
- Nomes claros do domínio do projeto
- Descrição concisa de 1-2 linhas
- Lista de visão geral (não detalhada)

**Subgrupos:**
- Subdivisão lógica do grupo pai
- Aproximadamente 3-8 tarefas por subgrupo
- Coesão interna (tarefas relacionadas)
- Facilita implementação sequencial
