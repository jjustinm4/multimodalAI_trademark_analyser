export default function ClassificationPanel({ nice }) {
  const { top_classes: classes, provided_class: provided, matches_top: matches } = nice
  const max = Math.max(...classes.map((c) => c.confidence), 0.01)
  return (
    <section className="panel p-5">
      <h2 className="panel-title">Nice classification</h2>
      {provided != null && (
        <div className={`mt-3 flex items-start gap-2 rounded-md px-3 py-2 text-sm ${matches
          ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-500/10 dark:text-emerald-300'
          : 'bg-amber-50 text-amber-800 dark:bg-amber-500/10 dark:text-amber-300'}`}>
          <span aria-hidden>{matches ? '✓' : '⚠'}</span>
          <span>{matches
            ? `Stated class ${provided} matches the top suggestion.`
            : `Stated class ${provided} differs from the top suggestion (${classes[0]?.class_number}). Confirm classification.`}</span>
        </div>
      )}
      <ol className="mt-4 space-y-3">
        {classes.map((c, i) => (
          <li key={c.class_number}>
            <div className="flex items-baseline justify-between gap-2 text-sm">
              <span className="min-w-0 truncate">
                <span className="mr-2 font-mono font-semibold">{c.class_number}</span>
                <span className={i === 0 ? 'font-medium' : 'text-slate-600 dark:text-slate-400'}>{c.class_name}</span>
                {provided === c.class_number && <span className="ml-2 text-xs text-slate-500">(stated)</span>}
              </span>
              <span className="shrink-0 tabular-nums text-slate-500">{(c.confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="mt-1 h-1.5 rounded-full bg-slate-100 dark:bg-slate-800">
              <div className={`h-full rounded-full ${i === 0 ? 'bg-indigo-500' : 'bg-indigo-300 dark:bg-indigo-700'}`}
                style={{ width: `${(c.confidence / max) * 100}%` }} />
            </div>
          </li>
        ))}
      </ol>
      <p className="mt-3 text-xs text-slate-400">Confidence is cosine similarity to Nice reference entries.</p>
    </section>
  )
}
