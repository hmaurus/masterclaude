---
description: Cria e publica um post no LinkedIn (texto, com imagem ou com link)
argument-hint: "<descrição do post ou 'com imagem caminho/imagem.png'>"
allowed-tools:
  - mcp__plugin_linkedin_linkedin__linkedin_create_post
  - mcp__plugin_linkedin_linkedin__linkedin_create_post_with_image
  - mcp__plugin_linkedin_linkedin__linkedin_create_post_with_link
  - mcp__plugin_linkedin_linkedin__linkedin_check_status
  - Read
---

# LinkedIn Post

Crie e publique um post no LinkedIn seguindo estas etapas:

## Contexto obrigatório

Antes de criar qualquer conteúdo, consulte estes documentos de referência (se disponíveis no projeto atual):
- `docs/referencias/perfil-de-maurus.md` — tom pessoal, valores, estilo de comunicação
- `.agents/product-marketing-context.md` — posicionamento, brand voice, keywords
- `docs/referencias/social-content.md` — preferências de postagem LinkedIn

## Regras

- **Tom:** pessoal, opinativo, autêntico — nunca corporativo ou genérico
- **Links:** NÃO colocar links no corpo do post (LinkedIn reduz alcance). Mencionar que o link vai no primeiro comentário se necessário
- **Formato:** LinkedIn usa formato "little" — o MCP server escapa caracteres automaticamente
- **Imagens:** Se o usuário mencionar imagem, usar `linkedin_create_post_with_image` com o caminho absoluto do arquivo
- **Workflow:** SEMPRE exibir o rascunho completo para aprovação antes de postar

## Fluxo

1. Verificar status do token com `linkedin_check_status`
2. Se o usuário forneceu tema/conteúdo, redigir o post seguindo o tom e regras acima
3. Exibir rascunho para aprovação
4. Após aprovação, publicar usando o tool adequado:
   - Texto: `linkedin_create_post`
   - Com imagem: `linkedin_create_post_with_image`
   - Com link: `linkedin_create_post_with_link`
5. Retornar URL do post publicado

## Argumento

$ARGUMENTS
