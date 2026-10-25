import { useState } from 'react'
import LogoUpload from './LogoUpload.jsx'

export const NICE_CLASS_NAMES = [
  'Chemicals', 'Paints', 'Cosmetics and cleaning preparations', 'Lubricants and fuels', 'Pharmaceuticals',
  'Metal goods', 'Machinery', 'Hand tools', 'Computers and scientific devices', 'Medical apparatus',
  'Environmental control apparatus', 'Vehicles', 'Firearms and fireworks', 'Jewelry', 'Musical instruments',
  'Paper goods and printed matter', 'Rubber goods', 'Leather goods', 'Non-metallic building materials', 'Furniture',
  'Housewares and glass', 'Ropes and fibres', 'Yarns and threads', 'Fabrics', 'Clothing', 'Fancy goods',
  'Floor coverings', 'Toys and sporting goods', 'Meats and processed foods', 'Staple foods',
  'Natural agricultural products', 'Light beverages', 'Wines and spirits', "Smokers' articles",
  'Advertising and business services', 'Insurance and financial services', 'Construction and repair services',
  'Telecommunications', 'Transportation and storage', 'Treatment of materials', 'Education and entertainment',
  'Computer and scientific services', 'Hotels and restaurants', 'Medical and beauty services',
  'Personal and legal services',
]

const EXAMPLES = [
  { mark_text: 'Zentrix', goods_description: 'software as a service for project management and team collaboration' },
  { mark_text: 'Champagne Nights', goods_description: 'restaurant and bar services' },
  { mark_text: 'Fresh Coffee', goods_description: 'coffee and tea' },
]

export default function SearchForm({ onSubmit, busy }) {
  const [markText, setMarkText] = useState('')
  const [goods, setGoods] = useState('')
  const [niceClass, setNiceClass] = useState('')
  const [logo, setLogo] = useState(null)
  const [quickMode, setQuickMode] = useState(false)

  const canSubmit = markText.trim() && (quickMode || goods.trim()) && !busy

  const submit = (e) => {
    e.preventDefault()
    if (!canSubmit) return
    onSubmit(
      {
        mark_text: markText.trim(),
        goods_description: goods.trim(),
        nice_class: niceClass ? Number(niceClass) : null,
        logo_file: logo?.dataUrl || null,
      },
      quickMode,
    )
  }

  return (
    <form onSubmit={submit} className="panel grid gap-6 p-6 lg:grid-cols-[1fr_260px]">
      <div className="space-y-5">
        <div>
          <label htmlFor="mark" className="mb-1.5 block text-sm font-medium">Mark <span className="text-red-500">*</span></label>
          <input id="mark" className="input text-lg font-semibold" placeholder="e.g. ZENTARA" value={markText}
            onChange={(e) => setMarkText(e.target.value)} maxLength={120} autoFocus />
        </div>
        <div>
          <label htmlFor="goods" className="mb-1.5 block text-sm font-medium">
            Goods / services {!quickMode && <span className="text-red-500">*</span>}
          </label>
          <textarea id="goods" rows={3} className="input resize-y" disabled={quickMode}
            placeholder="e.g. downloadable mobile application for tracking fitness goals" value={goods}
            onChange={(e) => setGoods(e.target.value)} maxLength={2000} />
          <div className="mt-1.5 flex flex-wrap gap-2 text-xs text-slate-500">
            <span>Try:</span>
            {EXAMPLES.map((ex) => (
              <button type="button" key={ex.mark_text} className="underline decoration-dotted hover:text-blue-600"
                onClick={() => { setMarkText(ex.mark_text); setGoods(ex.goods_description) }}>
                {ex.mark_text}
              </button>
            ))}
          </div>
        </div>
        <div className="max-w-sm">
          <label htmlFor="cls" className="mb-1.5 block text-sm font-medium">Nice class <span className="font-normal text-slate-500">(optional override)</span></label>
          <select id="cls" className="input" value={niceClass} onChange={(e) => setNiceClass(e.target.value)} disabled={quickMode}>
            <option value="">Suggest automatically</option>
            {NICE_CLASS_NAMES.map((name, i) => (
              <option key={i + 1} value={i + 1}>{i + 1} — {name}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className={quickMode ? 'pointer-events-none opacity-40' : ''}>
          <span className="mb-1.5 block text-sm font-medium">Logo <span className="font-normal text-slate-500">(optional)</span></span>
          <LogoUpload value={logo} onChange={setLogo} />
        </div>
        <div className="mt-auto space-y-3">
          <label className="flex cursor-pointer items-center gap-2.5 text-sm">
            <button type="button" role="switch" aria-checked={quickMode} onClick={() => setQuickMode(!quickMode)}
              className={`relative h-5 w-9 rounded-full transition ${quickMode ? 'bg-blue-600' : 'bg-slate-300 dark:bg-slate-700'}`}>
              <span className={`absolute top-0.5 h-4 w-4 rounded-full bg-white shadow transition ${quickMode ? 'left-[18px]' : 'left-0.5'}`} />
            </button>
            <span>Quick search <span className="text-slate-500">(phonetic + semantic, no report)</span></span>
          </label>
          <button type="submit" disabled={!canSubmit} className="btn-primary w-full py-3 text-base">
            {busy ? 'Working…' : quickMode ? 'Search' : 'Analyze'}
          </button>
        </div>
      </div>
    </form>
  )
}
