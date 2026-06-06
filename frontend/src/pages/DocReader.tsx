import { useState, useRef } from 'react'

const DOC_TYPES = ['보험 약관', '대출 문서', '금융 안내서', '예금/적금 상품', 'ELS/펀드 상품', '기타 금융 문서']

const EXAMPLES: Record<string, string> = {
  '보험 약관': `이 상품은 보험금의 지급과 관련\n보험자는 피보험자가 보험기간 중 급격하고 우연한 외래의 사고로 인해 신체에 손해를 입은 경우, 그 손해에 대하여 사망하거나 후유\n장해가 발생한 경우 보험금을 지급합니다. 단, 고지의무 위반 시 계약이 해지될 수 있습니다.`,
  '대출 문서': `이 상품은 변동금리 주택담보대출로, 금융사 6개월 기준금리에 연동되어 6개월마다 대출금리가 변경됩니다. 중도상환 시 잔여 대출원금의 1.2%에 해당하는 중도\n상환수수료가 부과됩니다.`,
  '예금/적금 상품': `이 상품은 자유적립식 정기적금으로 계약기간은 12개월, 24개월, 36개월 중 선택 가능합니다. 기본금리는 연 3.5%이며, 자동이체 납입 시 0.2%p 우대, 만기 시 원금과 이자를 일괄 지급합니다.`,
  'ELS/펀드 상품': `이 ELS는 KOSPI200 지수를 기초자산으로 하며, 6개월마다 조기상환 기회가 제공됩니다. 최초 기준가의 85% 이상 유지 시 연 6.5% 수익, 50% 미만 시 원금 손실 가능한 고위험 상품입니다.`,
}

interface Result { summary: string; easy: string; key: string; caution: string }

function HeroRobot() {
  return (
    <svg viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-44 h-52 drop-shadow-lg">
      <circle cx="100" cy="160" r="85" fill="#EDE9FE" opacity="0.6"/>
      <ellipse cx="100" cy="226" rx="38" ry="7" fill="#CBD5E1" opacity="0.25"/>
      <rect x="78" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="105" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="58" y="122" width="84" height="78" rx="22" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M142 130 Q162 118 168 108 Q172 100 165 96 Q158 92 153 102 Q148 112 142 120" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="22" y="134" width="36" height="18" rx="9" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M86 142 L100 133 L114 142 L114 157 Q100 167 86 157 Z" fill="#7C3AED"/>
      <path d="M94 151 L99 156 L111 144" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <rect x="61" y="57" width="78" height="71" rx="24" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="70" y="69" width="60" height="42" rx="12" fill="#0F172A"/>
      <circle cx="88"  cy="87" r="6.5" fill="#C4B5FD"/>
      <circle cx="88"  cy="87" r="3.2" fill="#A78BFA"/>
      <circle cx="112" cy="87" r="6.5" fill="#C4B5FD"/>
      <circle cx="112" cy="87" r="3.2" fill="#A78BFA"/>
      <circle cx="86"  cy="85" r="1.8" fill="white" opacity="0.6"/>
      <circle cx="110" cy="85" r="1.8" fill="white" opacity="0.6"/>
      <path d="M84 105 Q100 114 116 105" stroke="#C4B5FD" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
      <line x1="100" y1="57" x2="100" y2="40" stroke="#94A3B8" strokeWidth="2.5" strokeLinecap="round"/>
      <circle cx="100" cy="35" r="6" fill="#7C3AED"/>
      <circle cx="100" cy="35" r="3" fill="#DDD6FE"/>
    </svg>
  )
}

export default function DocReader() {
  const [mode, setMode] = useState<'text' | 'file'>('text')
  const [docType, setDocType] = useState('보험 약관')
  const [text, setText] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const fileRef = useRef<HTMLInputElement>(null)

  const analyze = async () => {
    setLoading(true); setError(''); setResult(null)
    try {
      const fd = new FormData()
      fd.append('doc_type', docType)
      if (mode === 'file' && file) fd.append('file', file)
      else fd.append('text', text)
      const r = await fetch('/api/doc-reader', { method: 'POST', body: fd })
      if (!r.ok) throw new Error(await r.text())
      setResult(await r.json())
    } catch {
      setError('AI 서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen">

      {/* Hero */}
      <div className="bg-gradient-to-br from-[#F3E8FF] via-[#EDE9FE] to-[#F5F3FF] px-8 py-10">
        <div className="max-w-4xl flex items-center justify-between gap-6">
          <div>
            <h1 className="text-3xl font-black text-[#3B0764] mb-2 leading-tight">문서 쉽게<br/>이해하기</h1>
            <p className="text-violet-700 text-sm leading-relaxed">
              어려운 금융 문서를 붙여넣으면<br/>AI가 쉬운 말로 풀어서 설명해드립니다
            </p>
          </div>
          <div className="relative flex-shrink-0 mr-4">
            <HeroRobot />
            {/* 문서 */}
            <div className="absolute -top-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-16 h-14 flex items-center justify-center animate-float-2">
              <svg viewBox="0 0 32 32" fill="none" className="w-9 h-9">
                <rect x="6" y="3" width="20" height="26" rx="3" stroke="#7C3AED" strokeWidth="2"/>
                <line x1="10" y1="10" x2="22" y2="10" stroke="#7C3AED" strokeWidth="1.8" strokeLinecap="round"/>
                <line x1="10" y1="15" x2="22" y2="15" stroke="#7C3AED" strokeWidth="1.8" strokeLinecap="round"/>
                <line x1="10" y1="20" x2="17" y2="20" stroke="#7C3AED" strokeWidth="1.8" strokeLinecap="round"/>
              </svg>
            </div>
            {/* 보호막 */}
            <div className="absolute top-[38%] -right-2 w-11 h-11 bg-violet-500 rounded-xl flex items-center justify-center shadow-lg animate-float-3">
              <svg viewBox="0 0 20 20" fill="none" className="w-6 h-6">
                <circle cx="8.5" cy="8.5" r="5.5" stroke="white" strokeWidth="2"/>
                <line x1="13" y1="13" x2="18" y2="18" stroke="white" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
            {/* 번개/즉시 */}
            <div className="absolute -bottom-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-14 h-12 flex items-center justify-center animate-float-4">
              <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
                <path d="M18 4 L10 18 L16 18 L14 28 L22 14 L16 14 Z"
                  fill="#A78BFA" stroke="#7C3AED" strokeWidth="1.5" strokeLinejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Main */}
      <div className="px-8 py-6">
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5 mb-5">

          {/* LEFT */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="text-violet-500 text-lg">📄</span>
              <h2 className="font-bold text-gray-800 text-base">문서 입력</h2>
            </div>

            <div className="space-y-4 mb-6">
              {[
                { bg: 'bg-violet-100',  icon: '📋', title: '핵심 요약',       desc: '긴 문서의 핵심 내용을 3문장으로 요약' },
                { bg: 'bg-purple-100',  icon: '💬', title: '쉬운 설명',        desc: '어려운 금융 용어를 일상 언어로 풀어 설명' },
                { bg: 'bg-indigo-100',  icon: '⚠️', title: '주의사항 추출',    desc: '놓치기 쉬운 중요 조건·위험 요소 강조' },
              ].map(f => (
                <div key={f.title} className="flex items-center gap-3">
                  <div className={`w-10 h-10 ${f.bg} rounded-full flex items-center justify-center text-lg flex-shrink-0`}>{f.icon}</div>
                  <div>
                    <p className="text-sm font-semibold text-gray-800">{f.title}</p>
                    <p className="text-xs text-gray-400">{f.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* 체크리스트 */}
            <div className="flex gap-2 mb-4">
              {(['text', 'file'] as const).map(m => (
                <button key={m} onClick={() => setMode(m)}
                  className={`flex-1 py-2 rounded-xl text-sm font-medium transition-all ${
                    mode === m ? 'bg-violet-600 text-white shadow' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}>
                  {m === 'text' ? '⌨️ 텍스트 입력' : '📎 파일 첨부'}
                </button>
              ))}
            </div>

            <div className="mb-4">
              <label className="label">문서 유형</label>
              <select className="input-field" value={docType} onChange={e => setDocType(e.target.value)}>
                {DOC_TYPES.map(t => <option key={t}>{t}</option>)}
              </select>
            </div>

            {mode === 'text' ? (
              <>
                <p className="text-xs text-gray-500 mb-2 font-medium">예시 불러오기</p>
                <div className="flex flex-wrap gap-1.5 mb-3">
                  {Object.keys(EXAMPLES).map(k => (
                    <button key={k} onClick={() => { setText(EXAMPLES[k]); setDocType(k) }}
                      className="text-xs px-2.5 py-1 rounded-lg border border-violet-200 text-violet-700 hover:bg-violet-50 transition-colors">
                      📄 {k}
                    </button>
                  ))}
                </div>
                <textarea className="input-field resize-none" rows={8}
                  placeholder="분석할 금융 문서 내용을 여기에 붙여넣으세요."
                  value={text} onChange={e => setText(e.target.value)} />
              </>
            ) : (
              <div onClick={() => fileRef.current?.click()}
                className="border-2 border-dashed border-violet-200 hover:border-violet-400 rounded-xl p-10 text-center cursor-pointer transition-colors bg-violet-50">
                {file
                  ? <p className="text-violet-700 font-medium text-sm">📎 {file.name} ({(file.size / 1024).toFixed(1)} KB)</p>
                  : (
                    <>
                      <div className="w-12 h-12 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-3">
                        <span className="text-2xl">📁</span>
                      </div>
                      <p className="text-violet-600 font-medium text-sm">클릭하여 파일 업로드</p>
                      <p className="text-violet-400 text-xs mt-1">PDF, JPG, PNG 지원</p>
                    </>
                  )}
                <input ref={fileRef} type="file" accept=".pdf,.jpg,.jpeg,.png" className="hidden"
                  onChange={e => setFile(e.target.files?.[0] ?? null)} />
              </div>
            )}

            <button onClick={analyze}
              disabled={loading || (mode === 'text' ? !text.trim() : !file)}
              className="w-full mt-4 bg-violet-600 hover:bg-violet-700 active:bg-violet-800 text-white
                         rounded-xl py-3.5 font-bold text-sm transition-all
                         disabled:opacity-60 disabled:cursor-not-allowed
                         flex flex-col items-center gap-0.5">
              <span>🔍 AI 쉬운 설명 시작</span>
              <span className="text-xs font-normal text-violet-200">어려운 문서를 쉽게 풀어드립니다</span>
            </button>
          </div>

          {/* RIGHT */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="text-lg">📊</span>
              <h2 className="font-bold text-gray-800 text-base">AI 분석 결과</h2>
            </div>

            {loading && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-12 h-12 border-4 border-violet-100 border-t-violet-600 rounded-full animate-spin mb-4"/>
                <p className="text-gray-600 font-medium text-sm">AI가 문서를 분석 중입니다...</p>
                <p className="text-gray-400 text-xs mt-1">요약 → 쉬운 설명 → 주의사항 추출</p>
              </div>
            )}

            {error && <div className="alert-danger text-sm">{error}</div>}

            {!result && !loading && (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <div className="w-20 h-20 bg-violet-50 rounded-full flex items-center justify-center mb-4">
                  <svg viewBox="0 0 40 40" fill="none" className="w-10 h-10">
                    <rect x="10" y="6" width="20" height="26" rx="3" fill="#DDD6FE" stroke="#C4B5FD" strokeWidth="1.5"/>
                    <rect x="14" y="12" width="12" height="2.5" rx="1.25" fill="#7C3AED" opacity="0.5"/>
                    <rect x="14" y="17" width="9" height="2.5" rx="1.25" fill="#7C3AED" opacity="0.4"/>
                    <rect x="14" y="22" width="10" height="2.5" rx="1.25" fill="#7C3AED" opacity="0.3"/>
                    <circle cx="27" cy="28" r="7" fill="#EDE9FE" stroke="#C4B5FD" strokeWidth="1.5"/>
                    <path d="M24.5 28 L26.5 30 L30 26" stroke="#7C3AED" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                  </svg>
                </div>
                <p className="font-semibold text-gray-600 text-sm mb-1">분석 결과가 없습니다</p>
                <p className="text-xs text-gray-400 leading-relaxed">왼쪽에 문서 내용을 입력하고<br/>시작 버튼을 눌러주세요</p>
              </div>
            )}

            {result && (
              <div className="space-y-4">
                <div className="border border-violet-100 bg-violet-50 rounded-xl p-4">
                  <p className="text-xs font-bold text-violet-700 mb-2">📋 핵심 요약</p>
                  <p className="text-sm text-violet-900 leading-relaxed">{result.summary}</p>
                </div>

                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-xs font-bold text-gray-500 mb-2">💬 쉽게 말하면</p>
                  <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">{result.easy}</p>
                </div>

                {result.key && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">✅ 꼭 알아야 할 내용</p>
                    <div className="alert-success whitespace-pre-wrap text-sm">{result.key}</div>
                  </div>
                )}

                {result.caution && result.caution !== '식별된 주의사항 없음' && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">⚠️ 주의사항</p>
                    <div className="alert-warning whitespace-pre-wrap text-sm">{result.caution}</div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Tip bar */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-violet-100 rounded-full flex items-center justify-center text-lg flex-shrink-0">💡</div>
            <div>
              <p className="text-sm font-semibold text-gray-800">문서 분석 팁</p>
              <p className="text-xs text-gray-500">분석 전에 꼭 살펴보세요. 어려운 용어가 많은 보험 약관이나 대출 문서도 AI가 쉽게 풀어드립니다.</p>
            </div>
          </div>
          <button className="flex items-center gap-1 text-xs text-violet-600 font-medium hover:underline flex-shrink-0 ml-4">
            더 알아보기
            <svg viewBox="0 0 16 16" fill="none" className="w-3.5 h-3.5">
              <path d="M6 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}

