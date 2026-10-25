import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchForm from '../components/SearchForm.jsx'
import SkeletonLoader from '../components/SkeletonLoader.jsx'
import StatusBadge from '../components/StatusBadge.jsx'
import { analyze, errorMessage, quickSearch, saveAnalysis } from '../api.js'

function QuickResults({ data, query }) {
  if (!data.results.length) return <p className="text-sm text-slate-500">No matches for “{query}”.</p>
  return (
    <div className="panel overflow-hidden">
      <div className="border-b border-slate-200 px-4 py-3 dark:border-slate-800">
        <span className="panel-title">Quick search · phonetic + semantic · {data.results.length} results</span>
      </div>
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-left text-xs text-slate-500 dark:bg-slate-800/50 dark:text-slate-400">
          <tr>
            <th className="px-4 py-2">Mark</th><th className="px-4 py-2">Class</th><th className="px-4 py-2">Goods</th>
            <th className="px-4 py-2">Status</th><th className="px-4 py-2 text-right">Phonetic</th>
            <th className="px-4 py-2 text-right">Semantic</th><th className="px-4 py-2 text-right">Similarity</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
          {data.results.map((r) => (
            <tr key={r.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
              <td className="px-4 py-2 font-semibold">{r.mark_text}</td>
              <td className="px-4 py-2 tabular-nums">{r.nice_class}</td>
              <td className="max-w-md truncate px-4 py-2 text-slate-600 dark:text-slate-400" title={r.goods}>{r.goods}</td>
              <td className="px-4 py-2"><StatusBadge status={r.status} /></td>
              <td className="px-4 py-2 text-right tabular-nums">{r.phonetic.toFixed(2)}</td>
              <td className="px-4 py-2 text-right tabular-nums">{r.semantic.toFixed(2)}</td>
              <td className="px-4 py-2 text-right font-semibold tabular-nums">{r.similarity.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function SearchPage() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [quick, setQuick] = useState(null)

  const onSubmit = async (form, quickMode) => {
    setError(null)
    setQuick(null)
    setLoading(quickMode ? 'quick' : 'full')
    try {
      if (quickMode) {
        setQuick({ data: await quickSearch(form.mark_text), query: form.mark_text })
      } else {
        const record = saveAnalysis({ ...(await analyze(form)), logo_preview: form.logo_file || null })
        navigate(`/results/${record.id}`, { state: record })
      }
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">New examination</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Search the register for conflicting marks, screen absolute grounds, suggest a Nice class, and draft a first-action report.
        </p>
      </div>
      <SearchForm onSubmit={onSubmit} busy={!!loading} />
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/50 dark:text-red-300">
          {error}
        </div>
      )}
      {loading === 'full' && <SkeletonLoader />}
      {loading === 'quick' && <p className="text-sm text-slate-500">Searching…</p>}
      {quick && <QuickResults {...quick} />}
    </div>
  )
}
