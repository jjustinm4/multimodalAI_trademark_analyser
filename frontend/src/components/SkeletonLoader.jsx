import { useEffect, useState } from 'react'

const STEPS = [
  'Running phonetic analysis...',
  'Computing semantic similarity...',
  'Comparing logos...',
  'Scoring goods proximity...',
  'Suggesting Nice classification...',
  'Screening absolute grounds...',
  'Retrieving precedent...',
  'Drafting report...',
]

// Progress is simulated: the backend returns everything in one response.
export default function SkeletonLoader() {
  const [step, setStep] = useState(0)
  useEffect(() => {
    const t = setInterval(() => setStep((s) => Math.min(s + 1, STEPS.length - 1)), 1100)
    return () => clearInterval(t)
  }, [])

  const bar = 'animate-pulse rounded bg-slate-200 dark:bg-slate-800'
  return (
    <div className="space-y-4" aria-live="polite">
      <div className="panel p-5">
        <ol className="space-y-1.5 text-sm">
          {STEPS.map((s, i) => (
            <li key={s} className={`flex items-center gap-2 ${i > step ? 'text-slate-400 dark:text-slate-600' : ''}`}>
              {i < step ? (
                <svg className="h-4 w-4 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"><path d="m5 12 5 5L20 7" /></svg>
              ) : i === step ? (
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-blue-500 border-t-transparent" />
              ) : (
                <span className="h-4 w-4 rounded-full border-2 border-slate-300 dark:border-slate-700" />
              )}
              {s}
            </li>
          ))}
        </ol>
      </div>
      <div className="grid gap-4 lg:grid-cols-[1fr_380px]">
        <div className="panel space-y-3 p-5">
          {[0, 1, 2, 3].map((i) => <div key={i} className={`${bar} h-20`} />)}
        </div>
        <div className="space-y-4">
          <div className={`panel h-40 ${bar}`} />
          <div className={`panel h-40 ${bar}`} />
        </div>
      </div>
    </div>
  )
}
