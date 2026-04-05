/**
 * Script de autenticação OAuth 2.0 com LinkedIn.
 * Executa uma vez para obter o access token e salvar em ~/.config/mcp-linkedin/.env.
 * Uso: node oauth.js
 */

import http from 'node:http'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { execFileSync } from 'node:child_process'

const CONFIG_DIR = path.join(os.homedir(), '.config', 'mcp-linkedin')
const ENV_PATH = path.join(CONFIG_DIR, '.env')

// Garante que o diretorio de config existe
if (!fs.existsSync(CONFIG_DIR)) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true })
}

// Carrega credenciais do app (CLIENT_ID/SECRET) do .env de config
let CLIENT_ID = process.env.LINKEDIN_CLIENT_ID
let CLIENT_SECRET = process.env.LINKEDIN_CLIENT_SECRET

if (!CLIENT_ID || !CLIENT_SECRET) {
  if (fs.existsSync(ENV_PATH)) {
    const env = fs.readFileSync(ENV_PATH, 'utf-8')
    const get = (key) => {
      const match = env.match(new RegExp(`^${key}="?([^"\\n]+)"?`, 'm'))
      return match?.[1] || ''
    }
    CLIENT_ID = CLIENT_ID || get('LINKEDIN_CLIENT_ID')
    CLIENT_SECRET = CLIENT_SECRET || get('LINKEDIN_CLIENT_SECRET')
  }
}

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error(`Erro: LINKEDIN_CLIENT_ID e LINKEDIN_CLIENT_SECRET devem estar em ${ENV_PATH}`)
  console.error(`\nCrie o arquivo com:\n`)
  console.error(`  LINKEDIN_CLIENT_ID="seu_client_id"`)
  console.error(`  LINKEDIN_CLIENT_SECRET="seu_client_secret"\n`)
  process.exit(1)
}

const REDIRECT_URI = 'http://localhost:3456/callback'
const SCOPES = 'openid profile w_member_social'
const STATE = Math.random().toString(36).substring(2, 15)

const authUrl =
  `https://www.linkedin.com/oauth/v2/authorization` +
  `?response_type=code` +
  `&client_id=${CLIENT_ID}` +
  `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}` +
  `&scope=${encodeURIComponent(SCOPES)}` +
  `&state=${STATE}`

console.log('\n--- LinkedIn OAuth ---\n')
console.log('Abra esta URL no navegador:\n')
console.log(authUrl)
console.log()

// Abre no navegador (WSL2: usa PowerShell)
try {
  execFileSync('powershell.exe', ['-NoProfile', '-c', `Start-Process '${authUrl}'`], { stdio: 'ignore' })
} catch {
  try {
    execFileSync('xdg-open', [authUrl], { stdio: 'ignore' })
  } catch {
    // URL já foi impressa acima
  }
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost:3456')

  if (url.pathname !== '/callback') {
    res.writeHead(404)
    res.end()
    return
  }

  const code = url.searchParams.get('code')
  const state = url.searchParams.get('state')
  const error = url.searchParams.get('error')

  if (error) {
    const desc = url.searchParams.get('error_description') || error
    res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' })
    res.end(`<h1>Erro</h1><p>${desc}</p>`)
    server.close()
    return
  }

  if (state !== STATE) {
    res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' })
    res.end('<h1>Erro: state mismatch</h1>')
    server.close()
    return
  }

  try {
    const tokenRes = await fetch('https://www.linkedin.com/oauth/v2/accessToken', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
        redirect_uri: REDIRECT_URI,
      }),
    })

    const tokenData = await tokenRes.json()

    if (tokenData.error) {
      throw new Error(`${tokenData.error}: ${tokenData.error_description}`)
    }

    const profileRes = await fetch('https://api.linkedin.com/v2/userinfo', {
      headers: { Authorization: `Bearer ${tokenData.access_token}` },
    })
    const profile = await profileRes.json()
    const personName = profile.name || profile.sub

    // Salva no .env de config
    let envContent = fs.existsSync(ENV_PATH) ? fs.readFileSync(ENV_PATH, 'utf-8') : ''

    const updates = {
      LINKEDIN_ACCESS_TOKEN: tokenData.access_token,
      LINKEDIN_PERSON_URN: profile.sub,
      LINKEDIN_TOKEN_EXPIRES_AT: new Date(Date.now() + tokenData.expires_in * 1000).toISOString(),
    }

    for (const [key, value] of Object.entries(updates)) {
      const regex = new RegExp(`^${key}=.*$`, 'm')
      if (regex.test(envContent)) {
        envContent = envContent.replace(regex, `${key}="${value}"`)
      } else {
        envContent += `\n${key}="${value}"`
      }
    }

    fs.writeFileSync(ENV_PATH, envContent.trim() + '\n')

    const expiresAt = new Date(Date.now() + tokenData.expires_in * 1000)

    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' })
    res.end(
      `<html><body style="font-family:system-ui;max-width:500px;margin:80px auto;text-align:center">` +
        `<h1>LinkedIn conectado!</h1>` +
        `<p><strong>Perfil:</strong> ${personName}</p>` +
        `<p><strong>Token expira em:</strong> ${expiresAt.toLocaleDateString('pt-BR')}</p>` +
        `<p style="color:#666">Credenciais salvas em ${ENV_PATH}</p>` +
        `<p style="color:#666">Pode fechar esta janela.</p>` +
        `</body></html>`
    )

    console.log(`\nConectado com sucesso!`)
    console.log(`  Perfil: ${personName}`)
    console.log(`  URN: ${profile.sub}`)
    console.log(`  Token expira em: ${expiresAt.toLocaleDateString('pt-BR')}`)
    console.log(`  Credenciais salvas em: ${ENV_PATH}\n`)
  } catch (err) {
    res.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' })
    res.end(`<h1>Erro ao obter token</h1><pre>${err.message}</pre>`)
    console.error('Erro:', err.message)
  }

  setTimeout(() => server.close(), 500)
})

server.listen(3456, () => {
  console.log('Aguardando callback em http://localhost:3456/callback ...\n')
})
