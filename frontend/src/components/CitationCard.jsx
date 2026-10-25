import { useState } from 'react'
import ScoreBar, { MATCHER_META } from './ScoreBar.jsx'
import StatusBadge, { ClassBadge } from './StatusBadge.jsx'
import { svgDataUrl } from '../api.js'

export function scoreColor(s) {
  if (s > 0.8) return 'text-red-600 dark:text-red-400'
  if (s >= 0.5) return 'text-amber-600 dark:text-amber-400'
  return 'text-emerald-600 dark:text-emerald-400'
}

export default function CitationCard({ citation: c, rank, weights }) {
  const [open, setOpen] = useState(false)
  return (
    <div className={`rounded-lg border transition ${open
      ? 'border-blue-300 bg-blue-50/40 dark:border-blue-800 dark:bg-blue-950/20'
      : 'border-slate-200 hover:border-slate-300 dark:border-slate-800 dark:hover:border-slate-700'}`}>
      <button type="button" onClick={() => setOpen(!open)} aria-expanded={open}
        className="flex w-full items-center gap-4 p-3 text-left">
        <span className="w-6 shrink-0 text-center font-mono text-sm text-slate-400">{rank}</span>
        {c.logo_svg ? (
          <img src={svgDataUrl(c.logo_svg)} alt="" className="h-12 w-12 shrink-0 rounded-md border border-slate-200 dark:border-slate-700" />
        ) : (
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md border border-dashed border-slate-200 text-[10px] text-slate-400 dark:border-slate-700">no logo</div>
        )}
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="truncate text-base font-semibold uppercase tracking-wide">{c.mark_text}</span>
            <ClassBadge n={c.nice_class} />
            <StatusBadge status={c.status} />
          </div>
          <p className="mt-0.5 truncate text-xs text-slate-500 dark:text-slate-400" title={c.goods_description}>{c.goods_description}</p>
          <div className="mt-2"><ScoreBar contributions={c.contributions} /></div>
        </div>
        <span className={`w-16 shrink-0 text-right text-2xl font-bold tabular-nums ${scoreColor(c.final_score)}`}>
          {c.final_score.toFixed(2)}
        </span>
      </button>
      {open && (
        <div className="border-t border-slate-200 px-4 pb-4 pt-3 text-sm dark:border-slate-800">
          <div className="grid grid-cols-4 gap-3">
            {Object.entries(MATCHER_META).map(([k, m]) => (
              <div key={k} className="rounded-md bg-white p-2.5 dark:bg-slate-900">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <span className={`h-2 w-2 rounded-sm ${m.color}`} />{m.label}
                </div>
                <div className="mt-1 text-lg font-semibold tabular-nums">{weights && !(k in weights) ? '—' : c.scores[k].toFixed(3)}</div>
                <div className="text-xs text-slate-500 tabular-nums">
                  {weights && k in weights ? `× ${weights[k].toFixed(3)} = ${c.contributions[k].toFixed(3)}` : 'not used'}
                </div>
              </div>
            ))}
          </div>
          <dl className="mt-3 grid grid-cols-[110px_1fr] gap-x-3 gap-y-1 text-xs">
            <dt className="text-slate-500">Registration ID</dt><dd className="font-mono">{c.id}</dd>
            <dt className="text-slate-500">Owner</dt><dd>{c.owner_name}</dd>
            <dt className="text-slate-500">Goods</dt><dd>{c.goods_description}</dd>
          </dl>
        </div>
      )}
    </div>
  )
}
