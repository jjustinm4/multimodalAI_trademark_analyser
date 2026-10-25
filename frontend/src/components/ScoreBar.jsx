export const MATCHER_META = {
  phonetic: { label: 'Phonetic', color: 'bg-phonetic', text: 'text-phonetic' },
  semantic: { label: 'Semantic', color: 'bg-semantic', text: 'text-semantic' },
  visual: { label: 'Visual', color: 'bg-visual', text: 'text-visual' },
  goods: { label: 'Goods', color: 'bg-goods', text: 'text-goods' },
}

// Stacked bar of weighted matcher contributions. Full width = a score of 1.0.
export default function ScoreBar({ contributions, height = 'h-2.5' }) {
  return (
    <div className={`flex w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800 ${height}`}>
      {Object.entries(MATCHER_META).map(([k, m]) => {
        const v = contributions?.[k] || 0
        if (v <= 0) return null
        return (
          <div key={k} className={m.color} style={{ width: `${Math.min(v, 1) * 100}%` }}
            title={`${m.label}: +${v.toFixed(3)}`} />
        )
      })}
    </div>
  )
}

export function ScoreLegend({ weights }) {
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500 dark:text-slate-400">
      {Object.entries(MATCHER_META).map(([k, m]) => (
        <span key={k} className={`flex items-center gap-1.5 ${weights && !(k in weights) ? 'opacity-40' : ''}`}>
          <span className={`h-2.5 w-2.5 rounded-sm ${m.color}`} />
          {m.label}
          {weights && (k in weights ? ` ${(weights[k] * 100).toFixed(1)}%` : ' (off)')}
        </span>
      ))}
    </div>
  )
}
