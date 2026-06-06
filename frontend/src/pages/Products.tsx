import { useState } from 'react'
import { useProfile } from '../context/ProfileContext'

const GOALS = ['단기 목돈 마련 (1~3년)', '중기 자산 증식 (3~10년)', '노후 생활 (10년 이상)', '안전한 자산 보호']
const RISK_LEVELS = ['매우 안전', '안전 추구', '중립', '수익 추구', '적극 투자']

interface Result {
  overall: string; short: string; long_term: string; retire: string;
  tax: string; easy: string; actions: string
}

function HeroRobot() {
  return (
    <svg viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-44 h-52 drop-shadow-lg">
      <circle cx="100" cy="160" r="85" fill="#D1FAE5" opacity="0.6"/>
      <ellipse cx="100" cy="226" rx="38" ry="7" fill="#CBD5E1" opacity="0.25"/>
      <rect x="78" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="105" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="58" y="122" width="84" height="78" rx="22" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M142 130 Q162 118 168 108 Q172 100 165 96 Q158 92 153 102 Q148 112 142 120" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="22" y="134" width="36" height="18" rx="9" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M86 142 L100 133 L114 142 L114 157 Q100 167 86 157 Z" fill="#059669"/>
      <path d="M94 151 L99 156 L111 144" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <rect x="61" y="57" width="78" height="71" rx="24" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="70" y="69" width="60" height="42" rx="12" fill="#0F172A"/>
      <circle cx="88"  cy="87" r="6.5" fill="#6EE7B7"/>
      <circle cx="88"  cy="87" r="3.2" fill="#34D399"/>
      <circle cx="112" cy="87" r="6.5" fill="#6EE7B7"/>
      <circle cx="112" cy="87" r="3.2" fill="#34D399"/>
      <circle cx="86"  cy="85" r="1.8" fill="white" opacity="0.6"/>
      <circle cx="110" cy="85" r="1.8" fill="white" opacity="0.6"/>
      <path d="M84 105 Q100 114 116 105" stroke="#6EE7B7" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
      <line x1="100" y1="57" x2="100" y2="40" stroke="#94A3B8" strokeWidth="2.5" strokeLinecap="round"/>
      <circle cx="100" cy="35" r="6" fill="#059669"/>
      <circle cx="100" cy="35" r="3" fill="#A7F3D0"/>
    </svg>
  )
}

export default function Products() {
  const { profile } = useProfile()
  const [goals, setGoals] = useState(['노후 생활 (10년 이상)'])
  const [riskLevel, setRiskLevel] = useState('안전 추구')
  const [monthlySave, setMonthlySave] = useState(50)
  const [hasPension, setHasPension] = useState('없음')
  const [hasIrp, setHasIrp] = useState('없음')
  const [taxConcern, setTaxConcern] = useState('보통')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const [tab, setTab] = useState(0)

  const toggleGoal = (g: string) =>
    setGoals(prev => prev.includes(g) ? prev.filter(x => x !== g) : [...prev, g])

  const recommend = async () => {
    if (!goals.length) return
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: profile.age, income: profile.income, asset: profile.asset,
          monthly_save: monthlySave, goals, risk_level: riskLevel,
          has_pension: hasPension, has_irp: hasIrp,
          tax_concern: taxConcern, has_loan: '없음',
        }),
      })
      if (!r.ok) throw new Error(await r.text())
      setResult(await r.json())
    } catch {
      setError('AI 서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
    } finally {
      setLoading(false)
    }
  }

  const TABS = [
    { label: '📈 단기 (1~3년)',      key: 'short' as const },
    { label: '💰 중기 (3~10년)',     key: 'long_term' as const },
    { label: '🏠 노후 (10년 이상)', key: 'retire' as const },
  ]

  return (
    <div className="min-h-screen">

      {/* Hero */}
      <div className="bg-gradient-to-br from-[#ECFDF5] via-[#D1FAE5] to-[#ECFDF5] px-8 py-10">
        <div className="max-w-4xl flex items-center justify-between gap-6">
          <div>
            <h1 className="text-3xl font-black text-[#064E3B] mb-2 leading-tight">맞춤 금융<br/>상품 추천</h1>
            <p className="text-emerald-700 text-sm leading-relaxed">
              나이, 자산, 투자 목표에 맞춰<br/>AI가 최적의 금융 상품을 추천해드립니다
            </p>
          </div>
          <div className="relative flex-shrink-0 mr-4">
            <HeroRobot />
            {/* 다이아몬드 */}
            <div className="absolute -top-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-16 h-14 flex items-center justify-center animate-float-2">
              <svg viewBox="0 0 32 32" fill="none" className="w-9 h-9">
                <path d="M16 5 L28 13 L16 27 L4 13 Z"
                  fill="#A7F3D0" stroke="#059669" strokeWidth="1.8" strokeLinejoin="round"/>
                <path d="M4 13 L10 9 L16 5 L22 9 L28 13" stroke="#059669" strokeWidth="1.5" fill="none" strokeLinejoin="round"/>
              </svg>
            </div>
            {/* 막대 차트 */}
            <div className="absolute top-[38%] -right-2 w-11 h-11 bg-emerald-500 rounded-xl flex items-center justify-center shadow-lg animate-float-3">
              <svg viewBox="0 0 20 20" fill="none" className="w-6 h-6">
                <rect x="2" y="12" width="3" height="6" rx="1" fill="white" opacity="0.7"/>
                <rect x="7" y="8"  width="3" height="10" rx="1" fill="white"/>
                <rect x="12" y="5" width="3" height="13" rx="1" fill="white"/>
                <line x1="1" y1="18" x2="17" y2="18" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </div>
            {/* 안전 */}
            <div className="absolute -bottom-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-14 h-12 flex items-center justify-center animate-float-4">
              <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
                <ellipse cx="16" cy="22" rx="10" ry="4" fill="#A7F3D0" stroke="#059669" strokeWidth="1.5"/>
                <ellipse cx="16" cy="18" rx="10" ry="4" fill="#A7F3D0" stroke="#059669" strokeWidth="1.5"/>
                <ellipse cx="16" cy="14" rx="10" ry="4" fill="#D1FAE5" stroke="#059669" strokeWidth="1.5"/>
                <text x="16" y="17" textAnchor="middle" fontSize="5" fill="#059669" fontWeight="bold">₩</text>
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
              <span className="text-emerald-500 text-lg">💎</span>
              <h2 className="font-bold text-gray-800 text-base">맞춤 조건 입력</h2>
            </div>

            <div className="space-y-4 mb-6">
              {[
                { bg: 'bg-emerald-100', icon: '🎯', title: '목표 분석',   desc: '재무 목표 및 투자 성향 기반 맞춤 분석' },
                { bg: 'bg-teal-100',    icon: '💎', title: '상품 매칭',   desc: 'JB금융그룹 상품 중 최적 포트폴리오 구성' },
                { bg: 'bg-green-100',   icon: '💡', title: '절세 추천',   desc: 'IRP·연금저축·비과세 상품 절세 전략 제안' },
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

            <div className="space-y-4">
              {/* 재무 목표 */}
              <div>
                <p className="label">🎯 재무 목표 (복수 선택 가능)</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {GOALS.map(g => (
                    <button key={g} onClick={() => toggleGoal(g)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                        goals.includes(g)
                          ? 'bg-emerald-600 text-white border-emerald-600'
                          : 'bg-white text-gray-600 border-gray-200 hover:border-emerald-300'
                      }`}>
                      {g}
                    </button>
                  ))}
                </div>
              </div>

              {/* 투자 성향 */}
              <div>
                <label className="label">투자 성향</label>
                <div className="flex gap-1">
                  {RISK_LEVELS.map(r => (
                    <button key={r} onClick={() => setRiskLevel(r)}
                      className={`flex-1 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                        riskLevel === r ? 'bg-emerald-600 text-white border-emerald-600' : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100'
                      }`}>
                      {r}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="label">월 저축금액 (만원)</label>
                  <input type="number" min={0} step={5} className="input-field"
                    value={monthlySave} onChange={e => setMonthlySave(Number(e.target.value))} />
                </div>
                <div>
                  <label className="label">여유자금</label>
                  <select className="input-field" value={hasPension} onChange={e => setHasPension(e.target.value)}>
                    {['없음', '미가입', '이미 가입'].map(v => <option key={v}>{v}</option>)}
                  </select>
                </div>
                <div>
                  <label className="label">IRP/연금저축</label>
                  <select className="input-field" value={hasIrp} onChange={e => setHasIrp(e.target.value)}>
                    {['없음', 'IRP 보유', '연금저축 보유', '둘 다 보유'].map(v => <option key={v}>{v}</option>)}
                  </select>
                </div>
                <div>
                  <label className="label">절세 관심 정도</label>
                  <select className="input-field" value={taxConcern} onChange={e => setTaxConcern(e.target.value)}>
                    {['걱정 없음', '보통', '매우 걱정됨'].map(v => <option key={v}>{v}</option>)}
                  </select>
                </div>
              </div>
            </div>

            <button onClick={recommend} disabled={loading || !goals.length}
              className="w-full mt-5 bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white
                         rounded-xl py-3.5 font-bold text-sm transition-all
                         disabled:opacity-60 disabled:cursor-not-allowed
                         flex flex-col items-center gap-0.5">
              <span>✨ AI 맞춤 상품 추천 받기</span>
              <span className="text-xs font-normal text-emerald-200">나에게 맞는 금융 상품을 찾아드립니다</span>
            </button>
          </div>

          {/* RIGHT */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="text-lg">💎</span>
              <h2 className="font-bold text-gray-800 text-base">AI 상품 추천</h2>
            </div>

            {loading && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-12 h-12 border-4 border-emerald-100 border-t-emerald-600 rounded-full animate-spin mb-4"/>
                <p className="text-gray-600 font-medium text-sm">AI가 맞춤 상품을 분석 중입니다...</p>
                <p className="text-gray-400 text-xs mt-1">목표 분석 → 상품 매칭 → 절세 전략</p>
              </div>
            )}

            {error && <div className="alert-danger text-sm">{error}</div>}

            {!result && !loading && (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <div className="w-20 h-20 bg-emerald-50 rounded-full flex items-center justify-center mb-4">
                  <svg viewBox="0 0 40 40" fill="none" className="w-10 h-10">
                    <path d="M20 8 L28 16 L20 36 L12 16 Z" fill="#A7F3D0" stroke="#6EE7B7" strokeWidth="1.5" strokeLinejoin="round"/>
                    <path d="M12 16 L20 8 L28 16" fill="#6EE7B7" opacity="0.7"/>
                    <circle cx="28" cy="10" r="4" fill="#34D399" opacity="0.6"/>
                    <circle cx="32" cy="20" r="3" fill="#34D399" opacity="0.4"/>
                  </svg>
                </div>
                <p className="font-semibold text-gray-600 text-sm mb-1">추천 결과가 없습니다</p>
                <p className="text-xs text-gray-400 leading-relaxed">왼쪽에서 목표 및 투자 성향을<br/>선택해주세요.</p>
              </div>
            )}

            {result && (
              <div className="space-y-4 overflow-y-auto max-h-[600px] pr-1">
                <div className="border border-emerald-100 bg-emerald-50 rounded-xl p-4">
                  <p className="text-xs font-bold text-emerald-700 mb-1">💎 종합 분석</p>
                  <p className="text-xs text-emerald-900 leading-relaxed">{result.overall}</p>
                </div>

                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-xs font-bold text-gray-500 mb-3">🎯 목표별 추천 상품</p>
                  <div className="flex gap-1 mb-3">
                    {TABS.map((t, i) => (
                      <button key={t.key} onClick={() => setTab(i)}
                        className={`flex-1 py-1.5 rounded-lg text-xs font-medium transition-all ${tab === i ? 'bg-emerald-600 text-white' : 'bg-gray-100 text-gray-600'}`}>
                        {t.label}
                      </button>
                    ))}
                  </div>
                  <div className="alert-success whitespace-pre-wrap text-sm min-h-[60px]">
                    {result[TABS[tab].key] || '해당 없음'}
                  </div>
                </div>

                {result.tax && result.tax !== '해당 없음' && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">💡 절세 상품 추천</p>
                    <div className="alert-warning whitespace-pre-wrap text-sm">{result.tax}</div>
                  </div>
                )}

                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-xs font-bold text-gray-500 mb-2">💬 쉽게 말하면</p>
                  <p className="text-xs text-gray-600 leading-relaxed">{result.easy}</p>
                </div>

                {result.actions && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">✅ 지금 해야 할 행동</p>
                    <div className="alert-success whitespace-pre-wrap text-sm">{result.actions}</div>
                  </div>
                )}

                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-xs font-bold text-gray-500 mb-3">📞 JB금융그룹 상담 연결</p>
                  <div className="grid grid-cols-2 gap-2">
                      {[['전북은행', '1588-4477'], ['광주은행', '1588-3388'], ['JB우리캐피탈', '1600-2266'], ['JB자산운용', '홈페이지']].map(([label, tel]) => (
                      <div key={label} className="alert-success text-center text-xs rounded-xl p-2.5">
                        <p className="font-bold">{label}</p>
                        <p className="text-xs mt-0.5">📞 {tel}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Tip bar */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center text-lg flex-shrink-0">💡</div>
            <div>
              <p className="text-sm font-semibold text-gray-800">상품 추천 팁</p>
              <p className="text-xs text-gray-500">투자 성향을 정확하게 선택할수록 나에게 맞는 상품을 추천받을 수 있습니다. IRP·연금저축은 절세 효과가 큽니다.</p>
            </div>
          </div>
          <button className="flex items-center gap-1 text-xs text-emerald-600 font-medium hover:underline flex-shrink-0 ml-4">
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

