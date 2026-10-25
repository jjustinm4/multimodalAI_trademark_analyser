import axios from 'axios'

export const api = axios.create({ baseURL: '/api', timeout: 180000 })

export const analyze = (body) => api.post('/analyze', body).then((r) => r.data)
export const quickSearch = (q) => api.get('/search', { params: { q } }).then((r) => r.data)
export const classify = (goods_description) => api.post('/classify', { goods_description }).then((r) => r.data)
export const listMarks = (params) => api.get('/marks', { params }).then((r) => r.data)
export const getMark = (id) => api.get(`/marks/${id}`).then((r) => r.data)
export const getHealth = () => api.get('/health', { timeout: 8000 }).then((r) => r.data)

export function errorMessage(err) {
  const detail = err?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => `${d.loc?.slice(-1)[0]}: ${d.msg}`).join('; ')
  if (err?.code === 'ECONNABORTED') return 'The request timed out.'
  return err?.message || 'Something went wrong.'
}

// Results live in sessionStorage so /results/:id survives a reload.
const KEY = (id) => `analysis:${id}`
export function saveAnalysis(result) {
  const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6)
  const record = { ...result, id, created_at: new Date().toISOString() }
  try { sessionStorage.setItem(KEY(id), JSON.stringify(record)) } catch (e) { /* storage full or blocked */ }
  return record
}
export function loadAnalysis(id) {
  try { return JSON.parse(sessionStorage.getItem(KEY(id))) } catch (e) { return null }
}

export const svgDataUrl = (svg) => `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`
