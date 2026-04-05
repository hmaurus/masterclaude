/**
 * MCP Server para LinkedIn — permite postar, editar e deletar posts no LinkedIn via Claude Code.
 * Ferramentas: linkedin_create_post, linkedin_create_post_with_image, linkedin_create_post_with_link,
 *              linkedin_edit_post, linkedin_delete_post, linkedin_check_status
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { z } from 'zod'

const CONFIG_DIR = path.join(os.homedir(), '.config', 'mcp-linkedin')
const ENV_PATH = path.join(CONFIG_DIR, '.env')
const LINKEDIN_API = 'https://api.linkedin.com'
const API_VERSION = '202603'

/**
 * Escapa caracteres reservados do formato "little" do LinkedIn.
 * Sem isso, caracteres como ( ) # * _ truncam ou quebram o post.
 * @param {string} text
 * @returns {string}
 */
function escapeLinkedInText(text) {
  return text.replace(/([|{}@[\]()<>#\\*_~])/g, '\\$1')
}

/** @returns {{ token: string, urn: string, expiresAt: string }} */
function loadCredentials() {
  if (!fs.existsSync(ENV_PATH)) {
    throw new Error(`Credenciais nao encontradas em ${ENV_PATH}. Execute: node oauth.js`)
  }

  const env = fs.readFileSync(ENV_PATH, 'utf-8')
  const get = (key) => {
    const match = env.match(new RegExp(`^${key}="?([^"\\n]+)"?`, 'm'))
    return match?.[1] || ''
  }

  const token = get('LINKEDIN_ACCESS_TOKEN')
  const urn = get('LINKEDIN_PERSON_URN')
  const expiresAt = get('LINKEDIN_TOKEN_EXPIRES_AT')

  if (!token || !urn) {
    throw new Error('Token nao encontrado. Execute: node oauth.js')
  }

  if (expiresAt && new Date(expiresAt) < new Date()) {
    throw new Error(`Token expirou em ${new Date(expiresAt).toLocaleDateString('pt-BR')}. Execute: node oauth.js`)
  }

  return { token, urn, expiresAt }
}

/**
 * Faz requisicoes autenticadas para a API do LinkedIn.
 * @param {string} endpoint
 * @param {object} options
 */
async function linkedinFetch(endpoint, options = {}) {
  const { token } = loadCredentials()

  const res = await fetch(`${LINKEDIN_API}${endpoint}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      'LinkedIn-Version': API_VERSION,
      'X-Restli-Protocol-Version': '2.0.0',
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (res.status === 201) {
    const postId = res.headers.get('x-restli-id') || ''
    return { success: true, postId }
  }

  if (res.status === 204) {
    return { success: true }
  }

  if (!res.ok) {
    const error = await res.text()
    throw new Error(`LinkedIn API ${res.status}: ${error}`)
  }

  const text = await res.text()
  return text ? JSON.parse(text) : { success: true }
}

// --- MCP Server ---

const server = new McpServer({
  name: 'linkedin',
  version: '2.0.0',
})

// Tool: Criar post de texto
server.tool(
  'linkedin_create_post',
  'Cria um post de texto no LinkedIn. Caracteres especiais sao escapados automaticamente.',
  {
    text: z.string().min(1).max(3000).describe('Texto do post (max 3000 caracteres)'),
    visibility: z.enum(['PUBLIC', 'CONNECTIONS']).default('PUBLIC').describe('Visibilidade do post'),
  },
  async ({ text, visibility }) => {
    try {
      const { urn } = loadCredentials()
      const escaped = escapeLinkedInText(text)

      const result = await linkedinFetch('/rest/posts', {
        method: 'POST',
        body: JSON.stringify({
          author: `urn:li:person:${urn}`,
          commentary: escaped,
          visibility,
          distribution: {
            feedDistribution: 'MAIN_FEED',
            targetEntities: [],
            thirdPartyDistributionChannels: [],
          },
          lifecycleState: 'PUBLISHED',
          isReshareDisabledByAuthor: false,
        }),
      })

      const postUrl = result.postId
        ? `https://www.linkedin.com/feed/update/${result.postId}`
        : 'https://www.linkedin.com/feed/'

      return {
        content: [
          {
            type: 'text',
            text: `Post publicado com sucesso!\nURL: ${postUrl}\nPost ID: ${result.postId}\n\nTexto:\n${text.substring(0, 200)}${text.length > 200 ? '...' : ''}`,
          },
        ],
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Erro: ${err.message}` }], isError: true }
    }
  }
)

// Tool: Criar post com imagem
server.tool(
  'linkedin_create_post_with_image',
  'Cria um post no LinkedIn com uma imagem anexada. Aceita caminho absoluto para arquivo de imagem (PNG, JPG, GIF, WEBP).',
  {
    text: z.string().min(1).max(3000).describe('Texto do post (max 3000 caracteres)'),
    image_path: z.string().min(1).describe('Caminho absoluto para o arquivo de imagem (PNG, JPG, GIF, WEBP)'),
    alt_text: z.string().optional().describe('Texto alternativo para acessibilidade (opcional)'),
    visibility: z.enum(['PUBLIC', 'CONNECTIONS']).default('PUBLIC').describe('Visibilidade do post'),
  },
  async ({ text, image_path, alt_text, visibility }) => {
    try {
      const { token, urn } = loadCredentials()
      const escaped = escapeLinkedInText(text)
      const author = `urn:li:person:${urn}`

      if (!fs.existsSync(image_path)) {
        throw new Error(`Arquivo nao encontrado: ${image_path}`)
      }

      const ext = path.extname(image_path).toLowerCase()
      const mimeTypes = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp' }
      const mime = mimeTypes[ext]
      if (!mime) {
        throw new Error(`Formato nao suportado: ${ext}. Use PNG, JPG, GIF ou WEBP`)
      }

      // 1. Inicializar upload
      const initRes = await fetch(`${LINKEDIN_API}/rest/images?action=initializeUpload`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'LinkedIn-Version': API_VERSION,
          'X-Restli-Protocol-Version': '2.0.0',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          initializeUploadRequest: { owner: author },
        }),
      })

      if (!initRes.ok) {
        const err = await initRes.text()
        throw new Error(`Falha ao inicializar upload: ${initRes.status} ${err}`)
      }

      const initData = await initRes.json()
      const uploadUrl = initData.value.uploadUrl
      const imageUrn = initData.value.image

      // 2. Upload do binario
      const imageBuffer = fs.readFileSync(image_path)

      const uploadRes = await fetch(uploadUrl, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': mime,
        },
        body: imageBuffer,
      })

      if (!uploadRes.ok) {
        const err = await uploadRes.text()
        throw new Error(`Falha no upload da imagem: ${uploadRes.status} ${err}`)
      }

      // 3. Criar post com a imagem
      const postBody = {
        author,
        commentary: escaped,
        visibility,
        distribution: {
          feedDistribution: 'MAIN_FEED',
          targetEntities: [],
          thirdPartyDistributionChannels: [],
        },
        content: {
          media: {
            id: imageUrn,
          },
        },
        lifecycleState: 'PUBLISHED',
        isReshareDisabledByAuthor: false,
      }

      if (alt_text) {
        postBody.content.media.altText = alt_text
      }

      const result = await linkedinFetch('/rest/posts', {
        method: 'POST',
        body: JSON.stringify(postBody),
      })

      const postUrl = result.postId
        ? `https://www.linkedin.com/feed/update/${result.postId}`
        : 'https://www.linkedin.com/feed/'

      return {
        content: [
          {
            type: 'text',
            text: `Post com imagem publicado!\nURL: ${postUrl}\nPost ID: ${result.postId}\nImagem: ${path.basename(image_path)}`,
          },
        ],
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Erro: ${err.message}` }], isError: true }
    }
  }
)

// Tool: Criar post com link/artigo
server.tool(
  'linkedin_create_post_with_link',
  'Cria um post no LinkedIn com preview de link/artigo. Caracteres especiais sao escapados automaticamente.',
  {
    text: z.string().min(1).max(3000).describe('Texto do post'),
    url: z.string().url().describe('URL do artigo/link'),
    title: z.string().optional().describe('Titulo do artigo (opcional, LinkedIn extrai automaticamente)'),
    description: z.string().optional().describe('Descricao do artigo (opcional)'),
    visibility: z.enum(['PUBLIC', 'CONNECTIONS']).default('PUBLIC').describe('Visibilidade do post'),
  },
  async ({ text, url, title, description, visibility }) => {
    try {
      const { urn } = loadCredentials()
      const escaped = escapeLinkedInText(text)

      const article = { source: url }
      if (title) article.title = title
      if (description) article.description = description

      const result = await linkedinFetch('/rest/posts', {
        method: 'POST',
        body: JSON.stringify({
          author: `urn:li:person:${urn}`,
          commentary: escaped,
          visibility,
          distribution: {
            feedDistribution: 'MAIN_FEED',
            targetEntities: [],
            thirdPartyDistributionChannels: [],
          },
          content: { article },
          lifecycleState: 'PUBLISHED',
          isReshareDisabledByAuthor: false,
        }),
      })

      const postUrl = result.postId
        ? `https://www.linkedin.com/feed/update/${result.postId}`
        : 'https://www.linkedin.com/feed/'

      return {
        content: [
          {
            type: 'text',
            text: `Post com link publicado!\nURL do post: ${postUrl}\nPost ID: ${result.postId}\nLink: ${url}`,
          },
        ],
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Erro: ${err.message}` }], isError: true }
    }
  }
)

// Tool: Editar post existente
server.tool(
  'linkedin_edit_post',
  'Edita o texto de um post existente no LinkedIn. Use o Post ID retornado ao criar o post.',
  {
    post_id: z
      .string()
      .min(1)
      .describe('Post ID/URN retornado ao criar o post (ex: urn:li:share:123456)'),
    text: z.string().min(1).max(3000).describe('Novo texto do post'),
  },
  async ({ post_id, text }) => {
    try {
      loadCredentials()
      const escaped = escapeLinkedInText(text)
      const encodedUrn = encodeURIComponent(post_id)

      await linkedinFetch(`/rest/posts/${encodedUrn}`, {
        method: 'POST',
        headers: { 'X-RestLi-Method': 'PARTIAL_UPDATE' },
        body: JSON.stringify({
          patch: {
            $set: { commentary: escaped },
          },
        }),
      })

      return {
        content: [
          {
            type: 'text',
            text: `Post editado com sucesso!\nPost ID: ${post_id}\n\nNovo texto:\n${text.substring(0, 200)}${text.length > 200 ? '...' : ''}`,
          },
        ],
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Erro: ${err.message}` }], isError: true }
    }
  }
)

// Tool: Deletar post
server.tool(
  'linkedin_delete_post',
  'Deleta um post do LinkedIn. Use o Post ID retornado ao criar o post.',
  {
    post_id: z
      .string()
      .min(1)
      .describe('Post ID/URN retornado ao criar o post (ex: urn:li:share:123456)'),
  },
  async ({ post_id }) => {
    try {
      loadCredentials()
      const encodedUrn = encodeURIComponent(post_id)

      await linkedinFetch(`/rest/posts/${encodedUrn}`, {
        method: 'DELETE',
        headers: { 'X-RestLi-Method': 'DELETE' },
      })

      return {
        content: [{ type: 'text', text: `Post deletado com sucesso!\nPost ID: ${post_id}` }],
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Erro: ${err.message}` }], isError: true }
    }
  }
)

// Tool: Verificar status do token
server.tool(
  'linkedin_check_status',
  'Verifica se o token do LinkedIn esta valido e mostra dias restantes ate expirar.',
  {},
  async () => {
    try {
      const { token, urn, expiresAt } = loadCredentials()

      const expiresDate = expiresAt ? new Date(expiresAt).toLocaleDateString('pt-BR') : 'desconhecido'
      const daysLeft = expiresAt ? Math.ceil((new Date(expiresAt).getTime() - Date.now()) / (1000 * 60 * 60 * 24)) : '?'

      const res = await fetch(`${LINKEDIN_API}/v2/userinfo`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      let name = ''
      if (res.ok) {
        const profile = await res.json()
        name = profile.name || ''
      }

      return {
        content: [
          {
            type: 'text',
            text:
              `LinkedIn ${res.ok ? 'conectado' : 'ERRO - token invalido'}!\n` +
              (name ? `  Nome: ${name}\n` : '') +
              `  URN: ${urn}\n` +
              `  Token expira: ${expiresDate} (${daysLeft} dias restantes)\n` +
              `  Credenciais: ${ENV_PATH}\n` +
              `  Status: ${res.ok ? 'OK' : `HTTP ${res.status}`}`,
          },
        ],
      }
    } catch (err) {
      return { content: [{ type: 'text', text: `Erro: ${err.message}` }], isError: true }
    }
  }
)

// Iniciar servidor
const transport = new StdioServerTransport()
await server.connect(transport)
