import { useEffect, useState } from 'react'
import { errorMessage, listMarks, svgDataUrl } from '../api.js'
import MarkDetail from './MarkDetail.jsx'
import { NICE_CLASS_NAMES } from './SearchForm.jsx'
import StatusBadge from './StatusBadge.jsx'

const PAGE_SIZE = 50
const COLUMNS = [
  { key: 'id', label: 'ID' }, { key: 'mark_text', label: 'Mark' }, { key: 'nice_class', label: 'Class' },
  { key: null, label: 'Goods / services' }, { key: 'owner_name', label: 'Owner' },
  { key: 'status', label: 'Status' }, { key: 'filing_date', label: 'Filed' },
]

export default function CorpusBrowser() {
  const [q, setQ] = useState('')
  const [debouncedQ, setDebouncedQ] = useState('')
  const [niceClass, setNiceClass] = useState('')
  const [status, setStatus] = useState('')
  const [hasLogo, setHasLogo] = useState('')
  const [sort, setSort] = useState({ key: 'id', order: 'asc' })
  const [page, setPage] = useState(1)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState(null)

  useEffect(() => {
    const t = setTimeout(() => setDebouncedQ(q.trim()), 250)
    return () => clearTimeout(t)
  }, [q])
  useEffect(() => setPage(1), [debouncedQ, niceClass, status, hasLogo, sort])

  useEffect(() => {
    let cancelled = false
    setError(null)
    listMarks({
      page, page_size: PAGE_SIZE, q: debouncedQ || undefined, nice_class: niceClass || undefined,
      status: status || undefined, has_logo: hasLogo || undefined, sort: sort.key, order: sort.order,
    })
      .then((d) => !cancelled && setData(d))
      .catch((e) => !cancelled && setError(errorMessage(e)))
    return () => { cancelled = true }
  }, [page, debouncedQ, niceClass, status, hasLogo, sort])

  const pages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1
  const toggleSort = (key) => key && setSort((s) => ({ key, order: s.key === key && s.order === 'asc' ? 'desc' : 'asc' }))

  return (
    <div className="panel overflow-hidden">
      <div className="flex flex-wrap items-center gap-3 border-b border-slate-200 p-4 dark:border-slate-800">
        <input className="input max-w-xs" placeholder="Search mark, goods or owner" value={q} onChange={(e) => setQ(e.target.value)} />
        <select className="input max-w-[220px]" value={niceClass} onChange={(e) => setNiceClass(e.target.value)}>
          <option value="">All classes</option>
          {NICE_CLASS_NAMES.map((n, i) => <option key={i} value={i + 1}>{i + 1} — {n}</option>)}
        </select>
        <select className="input max-w-[160px]" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All statuses</option>
          {['registered', 'pending', 'opposed', 'dead'].map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <select className="input max-w-[150px]" value={hasLogo} onChange={(e) => setHasLogo(e.target.value)}>
          <option value="">Any logo</option>
          <option value="true">With logo</option>
          <option value="false">Word only</option>
        </select>
        <span className="ml-auto text-sm tabular-nums text-slate-500">{data ? `${data.total.toLocaleString()} marks` : ''}</span>
      </div>
      {error && <p className="p-4 text-sm text-red-600">{error}</p>}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs text-slate-500 dark:bg-slate-800/50 dark:text-slate-400">
            <tr>
              <th className="w-12 px-4 py-2" />
              {COLUMNS.map((c) => (
                <th key={c.label} className={`px-4 py-2 font-medium ${c.key ? 'cursor-pointer select-none hover:text-slate-900 dark:hover:text-white' : ''}`}
                  onClick={() => toggleSort(c.key)}>
                  {c.label}{sort.key === c.key && (sort.order === 'asc' ? ' ↑' : ' ↓')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {data?.items.map((m) => (
              <tr key={m.id} onClick={() => setSelected(m.id)} className="cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/40">
                <td className="px-4 py-1.5">
                  {m.logo_svg ? <img src={svgDataUrl(m.logo_svg)} alt="" className="h-8 w-8 rounded" /> : <span className="block h-8 w-8" />}
                </td>
                <td className="px-4 py-1.5 font-mono text-xs text-slate-500">{m.id}</td>
                <td className="px-4 py-1.5 font-semibold">{m.mark_text}</td>
                <td className="px-4 py-1.5 tabular-nums">{m.nice_class}</td>
                <td className="max-w-md truncate px-4 py-1.5 text-slate-600 dark:text-slate-400" title={m.goods_description}>{m.goods_description}</td>
                <td className="whitespace-nowrap px-4 py-1.5 text-slate-600 dark:text-slate-400">{m.owner_name}</td>
                <td className="px-4 py-1.5"><StatusBadge status={m.status} /></td>
                <td className="whitespace-nowrap px-4 py-1.5 tabular-nums text-slate-600 dark:text-slate-400">{m.filing_date}</td>
              </tr>
            ))}
            {data && !data.items.length && (
              <tr><td colSpan={8} className="px-4 py-10 text-center text-slate-500">No marks match these filters.</td></tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between border-t border-slate-200 px-4 py-3 text-sm dark:border-slate-800">
        <button className="btn-ghost" disabled={page <= 1} onClick={() => setPage(page - 1)}>Previous</button>
        <span className="tabular-nums text-slate-500">Page {page} of {pages}</span>
        <button className="btn-ghost" disabled={page >= pages} onClick={() => setPage(page + 1)}>Next</button>
      </div>
      {selected != null && <MarkDetail id={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}
