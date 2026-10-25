const STYLES = {
  registered: 'bg-blue-50 text-blue-700 ring-blue-600/20 dark:bg-blue-500/10 dark:text-blue-300 dark:ring-blue-400/30',
  pending: 'bg-slate-100 text-slate-700 ring-slate-500/20 dark:bg-slate-500/15 dark:text-slate-300 dark:ring-slate-400/30',
  opposed: 'bg-amber-50 text-amber-800 ring-amber-600/20 dark:bg-amber-500/10 dark:text-amber-300 dark:ring-amber-400/30',
  dead: 'bg-slate-50 text-slate-400 ring-slate-300 line-through dark:bg-slate-800 dark:text-slate-500 dark:ring-slate-700',
}

export default function StatusBadge({ status }) {
  return <span className={`badge capitalize ${STYLES[status] || STYLES.pending}`}>{status}</span>
}

export function ClassBadge({ n, title }) {
  return (
    <span title={title} className="badge bg-indigo-50 font-mono text-indigo-700 ring-indigo-600/20 dark:bg-indigo-500/10 dark:text-indigo-300 dark:ring-indigo-400/30">
      Cl. {n}
    </span>
  )
}
