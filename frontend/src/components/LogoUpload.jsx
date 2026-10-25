import { useRef, useState } from 'react'

const ACCEPT = ['image/png', 'image/jpeg', 'image/svg+xml']
const MAX_BYTES = 5 * 1024 * 1024

export default function LogoUpload({ value, onChange }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [error, setError] = useState(null)

  const handleFile = (file) => {
    setError(null)
    if (!file) return
    if (!ACCEPT.includes(file.type)) return setError('Use a PNG, JPG or SVG file.')
    if (file.size > MAX_BYTES) return setError('File is larger than 5 MB.')
    const reader = new FileReader()
    reader.onload = () => onChange({ name: file.name, dataUrl: reader.result })
    reader.onerror = () => setError('Could not read the file.')
    reader.readAsDataURL(file)
  }

  if (value) {
    return (
      <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
        <img src={value.dataUrl} alt="Logo preview" className="h-20 w-20 rounded-md border border-slate-200 bg-white object-contain dark:border-slate-700" />
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium" title={value.name}>{value.name}</p>
          <button type="button" className="mt-1 text-xs text-red-600 hover:underline" onClick={() => onChange(null)}>Remove</button>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div
        role="button" tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files?.[0]) }}
        className={`flex h-36 cursor-pointer flex-col items-center justify-center gap-1 rounded-lg border-2 border-dashed text-center text-sm transition
          ${dragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-950/40' : 'border-slate-300 hover:border-slate-400 dark:border-slate-700 dark:hover:border-slate-500'}`}
      >
        <svg className="h-6 w-6 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2M12 4v12m0-12-4 4m4-4 4 4" /></svg>
        <span className="font-medium">Drop logo or click</span>
        <span className="text-xs text-slate-500">PNG, JPG or SVG</span>
      </div>
      <input ref={inputRef} type="file" accept=".png,.jpg,.jpeg,.svg" className="hidden"
        onChange={(e) => { handleFile(e.target.files?.[0]); e.target.value = '' }} />
      {error && <p className="mt-1.5 text-xs text-red-600">{error}</p>}
    </div>
  )
}
