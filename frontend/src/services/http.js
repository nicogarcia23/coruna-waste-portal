import { getAuthHeader } from './auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

export class ApiError extends Error {
  constructor(status, message, payload) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.payload = payload
  }
}

function buildUrl(path, query) {
  const url = new URL(`${API_BASE_URL}${path}`, window.location.origin)
  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, String(value))
      }
    })
  }
  return `${url.pathname}${url.search}`
}

export async function request(path, options = {}) {
  const {
    method = 'GET',
    query,
    body,
    headers = {},
    auth = false,
  } = options

  const response = await fetch(buildUrl(path, query), {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(auth ? getAuthHeader() : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  })

  const contentType = response.headers.get('content-type') || ''
  const payload = contentType.includes('application/json')
    ? await response.json()
    : await response.text()

  if (!response.ok) {
    const message =
      payload?.detail || payload?.message || payload || `Request failed with ${response.status}`
    throw new ApiError(response.status, message, payload)
  }

  return payload
}
