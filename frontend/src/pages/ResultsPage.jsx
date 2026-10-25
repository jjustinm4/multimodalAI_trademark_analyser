import { Link, useLocation, useParams } from 'react-router-dom'
import ResultsDashboard from '../components/ResultsDashboard.jsx'
import { loadAnalysis } from '../api.js'

export default function ResultsPage() {
  const { id } = useParams()
  const location = useLocation()
  const result = location.state?.id === id ? location.state : loadAnalysis(id)

  if (!result) {
    return (
      <div className="panel mx-auto max-w-lg p-8 text-center">
        <h1 className="text-lg font-semibold">Analysis not found</h1>
        <p className="mt-2 text-sm text-slate-500">Results are kept for this browser session only.</p>
        <Link to="/" className="btn-primary mt-6">Start a new examination</Link>
      </div>
    )
  }
  return <ResultsDashboard result={result} />
}
