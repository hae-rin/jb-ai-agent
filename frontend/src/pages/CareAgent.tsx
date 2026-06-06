import { useState } from 'react'
import { useProfile } from '../context/ProfileContext'

const TX_RISK_EXAMPLE = `2025-01-15 | 해외 송금 | 500만원 | 베트남 계좌
2025-01-15 | ATM 출금 | 200만원 | 강남역
2025-01-14 | 모르는 번호 송금 | 150만원 | 010-9999-1234
2025-01-13 | 온라인 쇼핑 | 8만원 | 쿠팡`

const TX_NORMAL_EXAMPLE = `2025-01-15 | 마트 | 8만원 | 이마트
2025-01-14 | 병원비 | 3만원 | 서울성모병원
2025-01-13 | 편의점 | 1만원 | GS25
2025-01-12 | 약국 | 1만원 | 온누리약국`

interface Result {
  fin_risk: string; fin_cashflow: string; fin_risks: string; fin_sustain: string
  has_tx: boolean; tx_risk: string; tx_signals: string
  핵심_메시지: string; immediate: string; short_plan: string; long_strategy: string
  corrections: string; final_summary: string; confidence: string
}

function RiskBadge({ level }: { level: string }) {
  if (level.includes('위험') || level.includes('높음'))
    return <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-bold">{level}</span>
  if (level.includes('주의') || level.includes('보통'))
    return <span className="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-sm font-bold">{level}</span>
  return <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-bold">{level}</span>
}

// Robot for hero
function HeroRobot() {
  return (
    <svg viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-44 h-52 drop-shadow-lg">
      <circle cx="100" cy="160" r="85" fill="#DBEAFE" opacity="0.4"/>
      <ellipse cx="100" cy="226" rx="38" ry="7" fill="#CBD5E1" opacity="0.25"/>
      <rect x="78" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="105" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="58" y="122" width="84" height="78" rx="22" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      {/* Waving arm (right) */}
      <path d="M142 130 Q162 118 168 108 Q172 100 165 96 Q158 92 153 102 Q148 112 142 120" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="22" y="134" width="36" height="18" rx="9" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M86 142 L100 133 L114 142 L114 157 Q100 167 86 157 Z" fill="#2563EB"/>
      <path d="M94 151 L99 156 L111 144" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <rect x="61" y="57" width="78" height="71" rx="24" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="70" y="69" width="60" height="42" rx="12" fill="#0F172A"/>
      <circle cx="88"  cy="87" r="6.5" fill="#38BDF8"/>
      <circle cx="88"  cy="87" r="3.2" fill="#0EA5E9"/>
      <circle cx="112" cy="87" r="6.5" fill="#38BDF8"/>
      <circle cx="112" cy="87" r="3.2" fill="#0EA5E9"/>
      <circle cx="86"  cy="85" r="1.8" fill="white" opacity="0.6"/>
      <circle cx="110" cy="85" r="1.8" fill="white" opacity="0.6"/>
      <path d="M84 105 Q100 114 116 105" stroke="#38BDF8" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
      <line x1="100" y1="57" x2="100" y2="40" stroke="#94A3B8" strokeWidth="2.5" strokeLinecap="round"/>
      <circle cx="100" cy="35" r="6" fill="#2563EB"/>
      <circle cx="100" cy="35" r="3" fill="#93C5FD"/>
    </svg>
  )
}

export default function CareAgent() {
  const { profile } = useProfile()
  const [transactions, setTransactions] = useState('')
  const [txOpen, setTxOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const [tab, setTab] = useState(0)

  const analyze = async () => {
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await fetch('/api/care-agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: profile.age, income: profile.income,
          asset: profile.asset, expense: profile.expense,
          transactions: transactions || null,
        }),
      })
      if (!r.ok) throw new Error(await r.text())
      setResult(await r.json())
    } catch {
      setError('AI 서버에 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
    } finally {
      setLoading(false)
    }
  }

  const downloadPdf = async () => {
    if (!result) return
    const r = await fetch('/api/care-agent/pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...result, age: profile.age, income: profile.income, asset: profile.asset, expense: profile.expense }),
    })
    const blob = await r.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url
    a.download = `Slowfit_리포트_${new Date().toISOString().slice(0,10)}.pdf`; a.click()
    URL.revokeObjectURL(url)
  }

  const isUrgent  = result && (result.fin_risk.includes('위험') || result.tx_risk.includes('높음'))
  const isCaution = result && (result.fin_risk.includes('주의') || result.tx_risk.includes('보통'))

  const PLAN_TABS = [
    { label: '⚡ 즉각 조치',  content: result?.immediate,     cls: 'alert-danger'  },
    { label: '📅 단기 계획',  content: result?.short_plan,    cls: 'alert-warning' },
    { label: '🔭 장기 전략',  content: result?.long_strategy, cls: 'alert-info'    },
  ]

  return (
    <div className="min-h-screen">

      {/* ── Hero ── */}
      <div className="bg-gradient-to-br from-[#EEF4FF] via-[#DBEAFE] to-[#EFF6FF] px-8 py-10">
        <div className="max-w-4xl flex items-center justify-between gap-6">
          <div>
            <h1 className="text-3xl font-black text-[#1E3A5F] mb-2 leading-tight">AI 종합 케어 에이전트</h1>
            <p className="text-gray-500 text-sm leading-relaxed">
              재무 상태, 거래 위험, 맞춤 케어 플랜까지<br/>AI가 단계별로 분석해드립니다.
            </p>
          </div>
          <div className="relative flex-shrink-0 mr-4">
            <HeroRobot/>
            <div className="absolute -top-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-16 h-14 flex items-center justify-center animate-float-2">
              <svg viewBox="0 0 32 32" fill="none" className="w-9 h-9">
                <rect x="4" y="18" width="6" height="10" rx="1.5" fill="#3B82F6"/>
                <rect x="13" y="12" width="6" height="16" rx="1.5" fill="#3B82F6"/>
                <rect x="22" y="6" width="6" height="22" rx="1.5" fill="#3B82F6"/>
              </svg>
            </div>
            <div className="absolute top-[38%] -right-2 w-11 h-11 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg animate-float-3">
              <svg viewBox="0 0 20 20" fill="none" className="w-6 h-6">
                <path d="M10 2L3 5.5v5C3 14.25 6.13 17.9 10 19c3.87-1.1 7-4.75 7-8.5v-5L10 2z" fill="white"/>
                <path d="M7 10l2 2 4-4" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="absolute -bottom-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-14 h-12 flex items-center justify-center animate-float-4">
              <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
                <circle cx="16" cy="16" r="12" stroke="#3B82F6" strokeWidth="2"/>
                <path d="M16 16 L16 6 A10 10 0 0 1 24 22 Z" fill="#3B82F6"/>
                <path d="M16 16 L8 20 A10 10 0 0 1 16 6 Z" fill="#93C5FD"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* ── Main content ── */}
      <div className="px-8 py-6">
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5 mb-5">

          {/* LEFT: AI 분석 시작하기 */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="text-blue-500 text-lg">✦</span>
              <h2 className="font-bold text-gray-800 text-base">AI 분석 시작하기</h2>
            </div>

            <div className="space-y-4 mb-6">
              {[
                { bg: 'bg-blue-100',    icon: '📊', title: '종합 분석',  desc: '재무 상태, 거래 패턴, 위험도 종합 분석' },
                { bg: 'bg-red-100',     icon: '🛡',  title: '위협 탐지',  desc: '이상 거래 및 금융 사기 위험 실시간 탐지' },
                { bg: 'bg-emerald-100', icon: '👤',  title: '맞춤 케어',  desc: '개인 맞춤형 금융 안전 관리 플랜 제공' },
              ].map(f => (
                <div key={f.title} className="flex items-center gap-3">
                  <div className={`w-10 h-10 ${f.bg} rounded-full flex items-center justify-center text-lg flex-shrink-0`}>
                    {f.icon}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-800">{f.title}</p>
                    <p className="text-xs text-gray-400">{f.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* 거래 내역 (선택) */}
            <button
              onClick={() => setTxOpen(o => !o)}
              className="w-full flex items-center justify-between text-sm font-medium text-gray-600
                         border border-dashed border-gray-200 rounded-xl px-4 py-2.5 mb-3
                         hover:bg-gray-50 transition-colors"
            >
              <span>📂 최근 거래 내역 입력 <span className="text-gray-400 font-normal">(선택)</span></span>
              <span className="text-gray-400 text-xs">{txOpen ? '▲' : '▼'}</span>
            </button>

            {txOpen && (
              <div className="mb-4 space-y-2">
                <div className="flex gap-2">
                  <button onClick={() => setTransactions(TX_RISK_EXAMPLE)}
                    className="flex-1 text-xs py-1.5 rounded-lg border border-red-200 text-red-600 hover:bg-red-50 transition-colors">
                    ⚠️ 위험 예시
                  </button>
                  <button onClick={() => setTransactions(TX_NORMAL_EXAMPLE)}
                    className="flex-1 text-xs py-1.5 rounded-lg border border-green-200 text-green-600 hover:bg-green-50 transition-colors">
                    ✅ 정상 예시
                  </button>
                </div>
                <textarea className="input-field resize-none text-sm" rows={5}
                  placeholder="날짜 | 항목 | 금액 | 수신처 형식으로 입력하세요."
                  value={transactions} onChange={e => setTransactions(e.target.value)} />
              </div>
            )}

            <button onClick={analyze} disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white
                         rounded-xl py-3.5 font-bold text-sm transition-all
                         disabled:opacity-60 disabled:cursor-not-allowed
                         flex flex-col items-center gap-0.5">
              <span>🤖 AI 에이전트 시작</span>
              <span className="text-xs font-normal text-blue-200">맞춤 분석을 시작해보세요</span>
            </button>
          </div>

          {/* RIGHT: AI 분석 결과 */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="text-lg">📋</span>
              <h2 className="font-bold text-gray-800 text-base">AI 분석 결과</h2>
            </div>

            {loading && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-12 h-12 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin mb-4"/>
                <p className="text-gray-600 font-medium text-sm">AI가 분석 중입니다...</p>
                <p className="text-gray-400 text-xs mt-1">재무 → 거래 → 케어 플랜 → 검증</p>
              </div>
            )}

            {error && <div className="alert-danger text-sm">{error}</div>}

            {!result && !loading && (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <div className="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mb-4">
                  <svg viewBox="0 0 40 40" fill="none" className="w-10 h-10">
                    <circle cx="18" cy="18" r="12" stroke="#93C5FD" strokeWidth="2.5"/>
                    <path d="M27 27 L34 34" stroke="#93C5FD" strokeWidth="2.5" strokeLinecap="round"/>
                    <circle cx="18" cy="18" r="6" fill="#DBEAFE"/>
                    <path d="M15 18 Q18 14 21 18" stroke="#60A5FA" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
                  </svg>
                </div>
                <p className="font-semibold text-gray-600 text-sm mb-1">아직 분석 결과가 없습니다</p>
                <p className="text-xs text-gray-400 leading-relaxed">왼쪽의 'AI 에이전트 시작' 버튼을 클릭하여<br/>맞춤 분석을 시작해보세요.</p>
              </div>
            )}

            {result && (
              <div className="space-y-4 overflow-y-auto max-h-[600px] pr-1">
                {/* 재무 분석 */}
                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-sm font-bold text-gray-500 mb-2">① 재무 건전성</p>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm text-gray-500">위험도</span>
                    <RiskBadge level={result.fin_risk} />
                  </div>
                  <p className="text-sm text-gray-600 leading-relaxed">{result.fin_cashflow}</p>
                  {result.fin_risks && result.fin_risks !== '위험 요인 없음' && (
                    <div className="alert-warning text-sm mt-2 whitespace-pre-wrap">{result.fin_risks}</div>
                  )}
                </div>

                {/* 거래 분석 */}
                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-sm font-bold text-gray-500 mb-2">② 거래 이상</p>
                  {result.has_tx ? (
                    <>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm text-gray-500">거래 위험도</span>
                        <RiskBadge level={result.tx_risk} />
                      </div>
                      {result.tx_signals && result.tx_signals !== '없음' && (
                        <div className="alert-warning text-sm whitespace-pre-wrap">{result.tx_signals}</div>
                      )}
                    </>
                  ) : (
                    <p className="text-sm text-gray-400">거래 내역 미입력</p>
                  )}
                </div>

                {/* 케어 플랜 */}
                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-sm font-bold text-gray-500 mb-2">③ 맞춤 케어 플랜</p>
                  {result.핵심_메시지 && (
                    <div className={`mb-3 rounded-lg p-3 text-sm font-medium ${isUrgent ? 'alert-danger' : isCaution ? 'alert-warning' : 'alert-success'}`}>
                      📌 {result.핵심_메시지}
                    </div>
                  )}
                  <div className="flex gap-1 mb-2">
                    {PLAN_TABS.map((t, i) => (
                      <button key={t.label} onClick={() => setTab(i)}
                        className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${tab === i ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600'}`}>
                        {t.label}
                      </button>
                    ))}
                  </div>
                  <div className={`text-sm whitespace-pre-wrap rounded-lg p-3 leading-relaxed ${PLAN_TABS[tab].cls}`}>
                    {PLAN_TABS[tab].content}
                  </div>
                </div>

                {/* 종합 + PDF */}
                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-sm font-bold text-gray-500 mb-2">④ 종합 리포트</p>
                  <div className="grid grid-cols-3 gap-2 mb-3">
                    {[['재무', result.fin_risk], ['거래', result.tx_risk], ['신뢰도', result.confidence]].map(([l, v]) => (
                      <div key={l} className="text-center">
                        <p className="text-sm text-gray-400 mb-1">{l}</p>
                        <RiskBadge level={v} />
                      </div>
                    ))}
                  </div>
                  <p className="text-sm text-gray-600 leading-relaxed mb-3">{result.final_summary}</p>
                  <button onClick={downloadPdf}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-3 text-sm font-semibold transition-colors">
                    📥 케어 리포트 PDF 다운로드
                  </button>
                </div>

                {/* JB 연계 */}
                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-sm font-bold text-gray-500 mb-3">🏦 JB금융그룹 연계</p>
                  <div className="grid grid-cols-2 gap-2">
                    {(isUrgent
                      ? [['전북은행', '1588-4477'], ['광주은행', '1588-3388']]
                      : [['전북은행', '1588-4477'], ['광주은행', '1588-3388'], ['JB우리캐피탈', '1600-2266'], ['JB자산운용', '홈페이지']]
                    ).map(([name, tel]) => (
                      <div key={name} className={`rounded-lg p-3 text-center text-sm ${isUrgent ? 'alert-danger' : 'alert-success'}`}>
                        <p className="font-bold">{name}</p>
                        <p className="mt-0.5">☎ {tel}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* ── Tip bar ── */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-lg flex-shrink-0">
              💡
            </div>
            <div>
              <p className="text-sm font-semibold text-gray-800">분석 팁</p>
              <p className="text-xs text-gray-500">정확한 분석을 위해 최근 거래 내역과 재무 정보를 입력해주세요. AI가 더 정확한 분석을 제공할 수 있습니다.</p>
            </div>
          </div>
          <button className="flex items-center gap-1 text-xs text-blue-600 font-medium hover:underline flex-shrink-0 ml-4">
            도움말 보기
            <svg viewBox="0 0 16 16" fill="none" className="w-3.5 h-3.5">
              <path d="M6 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}
