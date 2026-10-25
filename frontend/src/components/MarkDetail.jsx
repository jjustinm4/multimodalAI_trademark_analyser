import { useEffect, useState } from 'react'
import { errorMessage, getMark, svgDataUrl } from '../api.js'
import StatusBadge, { ClassBadge } from './StatusBadge.jsx'

export default function MarkDetail({ id, onClose }) {
  const [mark, setMark] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    setMark(null)
    setError(null)
    getMark(id).then(setMark).catch((e) => setError(errorMessage(e)))
  }, [id])

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && onClose()
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  return (
    <div className="fixed inset-0 z-30 flex items-center justify-center bg-slate-900/50 p-4" onClick={onClose}>
      <div className="panel w-full max-w-xl p-6" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        {error && <p className="text-sm text-red-600">{error}</p>}
        {!mark && !error && <div className="h-40 animate-pulse rounded bg-slate-100 dark:bg-slate-800" />}
        {mark && (
          <>
            <div className="flex items-start gap-4">
              {mark.logo_svg && <img src={svgDataUrl(mark.logo_svg)} alt="" className="h-24 w-24 rounded-md border border-slate-200 dark:border-slate-700" />}
              <div className="min-w-0 flex-1">
                <h2 className="text-xl font-bold uppercase tracking-wide">{mark.mark_text}</h2>
                <div className="mt-2 flex gap-2"><ClassBadge n={mark.nice_class} /><StatusBadge status={mark.status} /></div>
              </div>
              <button onClick={onClose} className="btn-ghost px-2.5 py-1" aria-label="Close">✕</button>
            </div>
            <dl className="mt-5 grid grid-cols-[130px_1fr] gap-x-4 gap-y-2 text-sm">
              <dt className="text-slate-500">ID</dt><dd className="font-mono">{mark.id}</dd>
              <dt className="text-slate-500">Goods / services</dt><dd>{mark.goods_description}</dd>
              <dt className="text-slate-500">Owner</dt><dd>{mark.owner_name}</dd>
              <dt className="text-slate-500">Filing date</dt><dd className="tabular-nums">{mark.filing_date}</dd>
              <dt className="text-slate-500">Phonetic keys</dt>
              <dd className="flex flex-wrap gap-1">{mark.phonetic_keys.map((k) => <code key={k} className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-xs dark:bg-slate-800">{k}</code>)}</dd>
            </dl>
          </>
        )}
      </div>
    </div>
  )
}
