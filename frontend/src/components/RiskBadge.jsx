export function riskLevel(score) {
  if (score > 0.8) return 'HIGH'
  if (score >= 0.5) return 'MEDIUM'
  return 'LOW'
}

const STYLES = {
  HIGH: 'bg-red-50 text-red-700 ring-red-600/25 dark:bg-red-500/15 dark:text-red-300 dark:ring-red-400/30',
  MEDIUM: 'bg-amber-50 text-amber-800 ring-amber-600/25 dark:bg-amber-500/15 dark:text-amber-300 dark:ring-amber-400/30',
  LOW: 'bg-emerald-50 text-emerald-700 ring-emerald-600/25 dark:bg-emerald-500/15 dark:text-emerald-300 dark:ring-emerald-400/30',
}

export default function RiskBadge({ score }) {
  const level = riskLevel(score)
  return <span className={`badge px-2.5 py-1 text-sm font-bold tracking-wide ${STYLES[level]}`}>{level} RISK</span>
}
