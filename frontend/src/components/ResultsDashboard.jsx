import { useState } from 'react'
import { Link } from 'react-router-dom'
import CitationCard from './CitationCard.jsx'
import ClassificationPanel from './ClassificationPanel.jsx'
import GroundsPanel from './GroundsPanel.jsx'
import ReportPanel from './ReportPanel.jsx'
import RiskBadge from './RiskBadge.jsx'
import { ScoreLegend } from './ScoreBar.jsx'
import { ClassBadge } from './StatusBadge.jsx'

function PrecedentPanel({ precedent }) {
  return (
    <section className="panel p-5">
      <h2 className="panel-title">Retrieved precedent</h2>
      {!precedent.length && <p className="mt-3 text-sm text-slate-500">None retrieved.</p>}
      <ul className="mt-3 space-y-3">
        {precedent.map((p) => (
          <li key={p.proceeding_number} className="text-sm">
            <div className="flex items-center justify-between gap-2">
              <span className="font-mono font-semibold">{p.proceeding_number}</span>
              <span className={`badge ${p.outcome === 'sustained'
                ? 'bg-red-50 text-red-700 ring-red-600/20 dark:bg-red-500/10 dark:text-red-300 dark:ring-red-400/30'
                : 'bg-slate-100 text-slate-600 ring-slate-500/20 dark:bg-slate-800 dark:text-slate-300 dark:ring-slate-600'}`}>
                {p.outcome}
              </span>
            </div>
            <p className="text-xs text-slate-500">{p.mark_a} v. {p.mark_b} · {p.decision_date} · sim {p.similarity.toFixed(2)}</p>
            <p className="mt-1 line-clamp-3 text-xs text-slate-600 dark:text-slate-400" title={p.excerpt}>{p.excerpt}</p>
          </li>
        ))}
      </ul>
    </section>
  )
}

export default function ResultsDashboard({ result }) {
  const { query, citations, weights } = result
  const [showAll, setShowAll] = useState(false)
  const top = citations[0]?.final_score ?? 0
  const shown = showAll ? citations : citations.slice(0, 10)

  return (
    <div className="space-y-5">
      <div className="panel flex flex-wrap items-center gap-4 px-5 py-4">
        {result.logo_preview && (
          <img src={result.logo_preview} alt="Applied-for logo" className="h-12 w-12 rounded-md border border-slate-200 bg-white object-contain dark:border-slate-700" />
        )}
        <div className="min-w-0">
          <h1 className="truncate text-2xl font-bold uppercase tracking-wide">{query.mark_text}</h1>
          <p className="truncate text-sm text-slate-500 dark:text-slate-400" title={query.goods_description}>{query.goods_description}</p>
        </div>
        {query.nice_class && (
          <ClassBadge n={query.nice_class} title={query.nice_class_source === 'provided' ? 'Stated by applicant' : 'Suggested'} />
        )}
        <RiskBadge score={top} />
        <div className="ml-auto text-right text-xs text-slate-500 dark:text-slate-400">
          <div>{new Date(result.created_at).toLocaleString()}</div>
          <div className="tabular-nums">Analysed in {(result.timings_ms.total / 1000).toFixed(1)}s</div>
        </div>
        <Link to="/" className="btn-ghost">New search</Link>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1fr_400px] lg:grid-cols-[1fr_340px]">
        <section className="panel p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 className="panel-title">Cited prior marks · {citations.length}</h2>
            <ScoreLegend weights={weights} />
          </div>
          <div className="mt-4 space-y-2">
            {shown.map((c, i) => <CitationCard key={c.id} citation={c} rank={i + 1} weights={weights} />)}
            {!citations.length && <p className="py-8 text-center text-sm text-slate-500">No conflicting marks found.</p>}
          </div>
          {citations.length > 10 && (
            <button onClick={() => setShowAll(!showAll)} className="btn-ghost mt-3 w-full">
              {showAll ? 'Show top 10' : `Show all ${citations.length}`}
            </button>
          )}
        </section>
        <aside className="space-y-5">
          <ClassificationPanel nice={result.nice_class} />
          <GroundsPanel grounds={result.grounds} />
          <PrecedentPanel precedent={result.precedent} />
        </aside>
      </div>

      <ReportPanel report={result.report} source={result.report_source} warning={result.report_warning} />
    </div>
  )
}
