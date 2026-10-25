import { useEffect, useState } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'
import SearchPage from './pages/SearchPage.jsx'
import ResultsPage from './pages/ResultsPage.jsx'
import BrowsePage from './pages/BrowsePage.jsx'
import { getHealth } from './api.js'

function HealthDot({ label, state }) {
  const color = state === 'ok' ? 'bg-emerald-500' : state ? 'bg-amber-500' : 'bg-slate-400'
  return (
    <span className="flex items-center gap-1.5" title={`${label}: ${state || 'checking'}`}>
      <span className={`h-2 w-2 rounded-full ${color}`} />
      {label}
    </span>
  )
}

function ThemeToggle() {
  const [dark, setDark] = useState(() => document.documentElement.classList.contains('dark'))
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])
  const toggle = () => {
    const next = !dark
    setDark(next)
    try { localStorage.setItem('theme', next ? 'dark' : 'light') } catch (e) { /* storage unavailable */ }
  }
  return (
    <button onClick={toggle} className="btn-ghost px-2.5 py-1.5" aria-label="Toggle dark mode">
      {dark ? (
        <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="4" /><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></svg>
      ) : (
        <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" /></svg>
      )}
    </button>
  )
}

export default function App() {
  const [health, setHealth] = useState({})
  useEffect(() => {
    const check = () => getHealth().then(setHealth).catch(() => setHealth({ db: 'unreachable', llm: 'unreachable' }))
    check()
    const t = setInterval(check, 30000)
    return () => clearInterval(t)
  }, [])

  const navClass = ({ isActive }) =>
    `rounded-md px-3 py-1.5 text-sm font-medium ${isActive
      ? 'bg-slate-200 text-slate-900 dark:bg-slate-800 dark:text-white'
      : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'}`

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">
        <div className="mx-auto flex h-14 max-w-[1800px] items-center gap-6 px-6">
          <NavLink to="/" className="flex items-center gap-2.5">
            <img src="/favicon.svg" alt="" className="h-7 w-7" />
            <span className="font-semibold tracking-tight">Examiner Console</span>
            <span className="badge bg-amber-50 text-amber-700 ring-amber-600/20 dark:bg-amber-400/10 dark:text-amber-300 dark:ring-amber-400/20">PoC · synthetic data</span>
          </NavLink>
          <nav className="flex gap-1">
            <NavLink to="/" end className={navClass}>Search</NavLink>
            <NavLink to="/browse" className={navClass}>Corpus</NavLink>
          </nav>
          <div className="ml-auto flex items-center gap-4 text-xs text-slate-500 dark:text-slate-400">
            <HealthDot label="DB" state={health.db} />
            <HealthDot label="LLM" state={health.llm} />
            <ThemeToggle />
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-[1800px] px-6 py-6">
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/results/:id" element={<ResultsPage />} />
          <Route path="/browse" element={<BrowsePage />} />
          <Route path="*" element={<p className="text-slate-500">Page not found.</p>} />
        </Routes>
      </main>
    </div>
  )
}
