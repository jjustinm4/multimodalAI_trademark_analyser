function Check({ label, flagged, evidence }) {
  return (
    <li className="flex items-start gap-3">
      <span className={`badge mt-0.5 shrink-0 ${flagged
        ? 'bg-red-50 text-red-700 ring-red-600/25 dark:bg-red-500/15 dark:text-red-300 dark:ring-red-400/30'
        : 'bg-emerald-50 text-emerald-700 ring-emerald-600/25 dark:bg-emerald-500/15 dark:text-emerald-300 dark:ring-emerald-400/30'}`}>
        {flagged ? 'FLAG' : 'CLEAR'}
      </span>
      <div className="min-w-0 text-sm">
        <p className="font-medium">{label}</p>
        {evidence && <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{evidence}</p>}
      </div>
    </li>
  )
}

export default function GroundsPanel({ grounds: g }) {
  const charFlag = g.flags.find((f) => f.startsWith('Single character') || f.startsWith('Purely numeric'))
  const prohibitedFlag = g.flags.find((f) => f.startsWith('Prohibited'))
  const dictCount = g.dictionary_tokens.length
  return (
    <section className="panel p-5">
      <h2 className="panel-title">Absolute grounds</h2>
      <ul className="mt-4 space-y-4">
        <Check label="Descriptiveness" flagged={g.descriptive}
          evidence={g.tokens.length
            ? `${dictCount} of ${g.tokens.length} word${g.tokens.length > 1 ? 's' : ''} found in dictionary${dictCount ? `: ${g.dictionary_tokens.join(', ')}` : ''}`
              + (g.tokens.length < 2 ? ' (single-word marks are not flagged)' : '')
            : null} />
        <Check label="Prohibited & protected terms" flagged={!!g.prohibited_match}
          evidence={prohibitedFlag ? prohibitedFlag.replace(/^Prohibited term: /, '') : 'No match at ≥85% similarity'} />
        <Check label="Single letter / numerals" flagged={!!charFlag}
          evidence={charFlag || 'Mark has more than one character and contains letters'} />
      </ul>
    </section>
  )
}
