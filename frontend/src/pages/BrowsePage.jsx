import CorpusBrowser from '../components/CorpusBrowser.jsx'

export default function BrowsePage() {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Corpus browser</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">All synthetic marks in the register. Click a row for details.</p>
      </div>
      <CorpusBrowser />
    </div>
  )
}
