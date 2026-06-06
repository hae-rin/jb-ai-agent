import { useState } from 'react'
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ReferenceLine, ResponsiveContainer, Legend, ReferenceArea,
} from 'recharts'
import { useProfile } from '../context/ProfileContext'
import { useAdaptive } from '../hooks/useAdaptive'

interface Result {
  risk: string; cashflow: string; pred_5: string; pred_10: string; pred_after: string
  actions: string; insight: string; easy: string
  monthly_shortage: number; sustain_years: number | null; assets_over_time: number[]
}

function HeroRobot() {
  return (
    <svg viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-44 h-52 drop-shadow-lg">
      <circle cx="100" cy="160" r="85" fill="#CFFAFE" opacity="0.5"/>
      <ellipse cx="100" cy="226" rx="38" ry="7" fill="#CBD5E1" opacity="0.25"/>
      <rect x="78" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="105" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="58" y="122" width="84" height="78" rx="22" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M142 130 Q162 118 168 108 Q172 100 165 96 Q158 92 153 102 Q148 112 142 120" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="22" y="134" width="36" height="18" rx="9" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M86 142 L100 133 L114 142 L114 157 Q100 167 86 157 Z" fill="#0891B2"/>
      <path d="M94 151 L99 156 L111 144" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <rect x="61" y="57" width="78" height="71" rx="24" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="70" y="69" width="60" height="42" rx="12" fill="#0F172A"/>
      <circle cx="88"  cy="87" r="6.5" fill="#67E8F9"/>
      <circle cx="88"  cy="87" r="3.2" fill="#22D3EE"/>
      <circle cx="112" cy="87" r="6.5" fill="#67E8F9"/>
      <circle cx="112" cy="87" r="3.2" fill="#22D3EE"/>
      <circle cx="86"  cy="85" r="1.8" fill="white" opacity="0.6"/>
      <circle cx="110" cy="85" r="1.8" fill="white" opacity="0.6"/>
      <path d="M84 105 Q100 114 116 105" stroke="#67E8F9" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
      <line x1="100" y1="57" x2="100" y2="40" stroke="#94A3B8" strokeWidth="2.5" strokeLinecap="round"/>
      <circle cx="100" cy="35" r="6" fill="#0891B2"/>
      <circle cx="100" cy="35" r="3" fill="#A5F3FC"/>
    </svg>
  )
}

export default function Simulation() {
  const { profile } = useProfile()
  const { isElder } = useAdaptive()
  const [healthStatus, setHealthStatus] = useState('양호')
  const [assetReal, setAssetReal] = useState('')
  const [medical, setMedical] = useState(30)
  const [hasFamily, setHasFamily] = useState('없음')
  const [hasLoan, setHasLoan] = useState('없음')
  const [familyContact, setFamilyContact] = useState('연락 가능')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const [tab, setTab] = useState(0)

  const simulate = async () => {
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await fetch('/api/simulation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: profile.age, health_status: healthStatus,
          asset_financial: profile.asset, income: profile.income,
          monthly_expense: profile.expense, medical,
          asset_real: assetReal, has_family: hasFamily,
          has_loan: hasLoan, family_contact: familyContact,
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

  const TABS = ['현재 ~ 5년', '5년 ~ 10년', '10년 이후']
  const tabContent = result ? [result.pred_5, result.pred_10, result.pred_after] : []

  return (
    <div className="min-h-screen">

      {/* Hero */}
      <div className="bg-gradient-to-br from-[#E0F7FA] via-[#B2EBF2] to-[#E0F2FE] px-8 py-10">
        <div className="max-w-4xl flex items-center justify-between gap-6">
          <div>
            <h1 className="text-3xl font-black text-[#164E63] mb-2 leading-tight">미래 생활 안정<br/>시뮬레이션</h1>
            <p className="text-cyan-700 text-sm leading-relaxed">
              {isElder
                ? '앞으로 생활비를 얼마나 버틸 수 있는지\nAI가 쉽게 알려드립니다.'
                : '자산·연금·생활비를 바탕으로\n노후 생활 안정성을 30년간 예측합니다'}
            </p>
          </div>
          <div className="relative flex-shrink-0 mr-4">
            <HeroRobot />
            {/* 꺾은선 그래프 */}
            <div className="absolute -top-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-16 h-14 flex items-center justify-center animate-float-2">
              <svg viewBox="0 0 32 32" fill="none" className="w-9 h-9">
                <polyline points="4,24 10,16 16,20 22,10 28,6"
                  stroke="#0891B2" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                <circle cx="28" cy="6" r="2.5" fill="#0891B2"/>
                <line x1="4" y1="26" x2="28" y2="26" stroke="#E2E8F0" strokeWidth="1.5"/>
              </svg>
            </div>
            {/* 저금/자산 */}
            <div className="absolute top-[38%] -right-2 w-11 h-11 bg-cyan-500 rounded-xl flex items-center justify-center shadow-lg animate-float-3">
              <svg viewBox="0 0 20 20" fill="none" className="w-6 h-6">
                <circle cx="10" cy="10" r="8" stroke="white" strokeWidth="1.5"/>
                <path d="M10 6v1m0 6v1M7.5 10c0-1.38 1.12-2.5 2.5-2.5s2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5"
                  stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </div>
            {/* 입력/기간 */}
            <div className="absolute -bottom-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-14 h-12 flex items-center justify-center animate-float-4">
              <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
                <rect x="4" y="6" width="24" height="22" rx="4" stroke="#0891B2" strokeWidth="2"/>
                <line x1="4" y1="13" x2="28" y2="13" stroke="#0891B2" strokeWidth="2"/>
                <line x1="10" y1="3" x2="10" y2="9" stroke="#0891B2" strokeWidth="2" strokeLinecap="round"/>
                <line x1="22" y1="3" x2="22" y2="9" stroke="#0891B2" strokeWidth="2" strokeLinecap="round"/>
                <circle cx="10" cy="20" r="2" fill="#0891B2"/>
                <circle cx="16" cy="20" r="2" fill="#0891B2"/>
                <circle cx="22" cy="20" r="2" fill="#0891B2"/>
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
              <span className="text-cyan-500 text-lg">📊</span>
              <h2 className="font-bold text-gray-800 text-base">시뮬레이션 설정</h2>
            </div>

            <div className="space-y-4 mb-6">
              {[
                { bg: 'bg-cyan-100',    icon: '💰', title: '현금흐름 분석',  desc: '월 수입·지출·의료비 기반 흑자/적자 계산' },
                { bg: 'bg-blue-100',    icon: '📈', title: '자산 장기 예측', desc: '30년간 금융 자산 증감 시뮬레이션' },
                { bg: 'bg-indigo-100',  icon: '⚠️', title: '위험 시나리오',  desc: '자산 소진 시점·위험 구간 미리 파악' },
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

            <div className="space-y-3 mb-5">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="label">건강 상태</label>
                  <select className="input-field" value={healthStatus} onChange={e => setHealthStatus(e.target.value)}>
                    {['양호', '보통', '주의 필요'].map(v => <option key={v}>{v}</option>)}
                  </select>
                </div>
                <div>
                  <label className="label">월 의료비 (만원)</label>
                  <input type="number" min={0} step={5} className="input-field"
                    value={medical} onChange={e => setMedical(Number(e.target.value))} />
                </div>
              </div>
              <div>
                <label className="label">부동산 자산 (선택)</label>
                <input className="input-field"
                  placeholder={isElder ? '예) 아파트 3억원' : '예) 아파트 3억원 (시가)'}
                  value={assetReal} onChange={e => setAssetReal(e.target.value)} />
              </div>
              {!isElder && (
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="label">가족 구성</label>
                    <select className="input-field" value={hasFamily} onChange={e => setHasFamily(e.target.value)}>
                      {['없음', '배우자', '자녀', '배우자+자녀'].map(v => <option key={v}>{v}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="label">부채</label>
                    <select className="input-field" value={hasLoan} onChange={e => setHasLoan(e.target.value)}>
                      {['없음', '있음 (소액)', '있음 (고액)'].map(v => <option key={v}>{v}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="label">보호자 연락</label>
                    <select className="input-field" value={familyContact} onChange={e => setFamilyContact(e.target.value)}>
                      {['연락 가능', '연락 어려움'].map(v => <option key={v}>{v}</option>)}
                    </select>
                  </div>
                </div>
              )}
            </div>

            <button onClick={simulate} disabled={loading}
              className="w-full bg-cyan-600 hover:bg-cyan-700 active:bg-cyan-800 text-white
                         rounded-xl py-3.5 font-bold text-sm transition-all
                         disabled:opacity-60 disabled:cursor-not-allowed
                         flex flex-col items-center gap-0.5">
              <span>🔮 {isElder ? 'AI 분석 시작' : 'AI 시뮬레이션 시작'}</span>
              <span className="text-xs font-normal text-cyan-200">30년 후 안정성을 예측합니다</span>
            </button>
          </div>

          {/* RIGHT */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="text-lg">📊</span>
              <h2 className="font-bold text-gray-800 text-base">시뮬레이션 결과</h2>
            </div>

            {loading && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-12 h-12 border-4 border-cyan-100 border-t-cyan-600 rounded-full animate-spin mb-4"/>
                <p className="text-gray-600 font-medium text-sm">AI가 미래를 분석 중입니다...</p>
                <p className="text-gray-400 text-xs mt-1">현금흐름 → 자산 예측 → 위험도 판정</p>
              </div>
            )}

            {error && <div className="alert-danger text-sm">{error}</div>}

            {!result && !loading && (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <div className="w-20 h-20 bg-cyan-50 rounded-full flex items-center justify-center mb-4">
                  <svg viewBox="0 0 40 40" fill="none" className="w-10 h-10">
                    <rect x="8" y="26" width="6" height="8" rx="2" fill="#A5F3FC"/>
                    <rect x="17" y="20" width="6" height="14" rx="2" fill="#67E8F9"/>
                    <rect x="26" y="14" width="6" height="20" rx="2" fill="#A5F3FC"/>
                    <path d="M6 32 Q14 24 22 26 Q30 28 36 16" stroke="#0891B2" strokeWidth="2" fill="none" strokeLinecap="round"/>
                  </svg>
                </div>
                <p className="font-semibold text-gray-600 text-sm mb-1">시뮬레이션 결과가 없습니다</p>
                <p className="text-xs text-gray-400 leading-relaxed">왼쪽 설정을 입력하고<br/>시뮬레이션을 시작해보세요.</p>
              </div>
            )}

            {result && (
              <div className="space-y-4 overflow-y-auto max-h-[600px] pr-1">
                <div className={`rounded-xl p-3 text-sm font-bold flex items-center gap-2
                  ${result.risk.includes('위험') ? 'alert-danger' : result.risk.includes('주의') ? 'alert-warning' : 'alert-success'}`}>
                  {result.risk.includes('위험') ? '🔴' : result.risk.includes('주의') ? '🟡' : '🟢'}
                  노후 생활 안정성: {result.risk}
                </div>

                {isElder && result.easy && (
                  <div className="border border-cyan-200 bg-cyan-50 rounded-xl p-3">
                    <p className="text-xs font-bold text-cyan-700 mb-1">📊 핵심 요약</p>
                    <p className="text-sm text-cyan-900 leading-relaxed">{result.easy}</p>
                  </div>
                )}

                {result.insight && (
                  <div className={`rounded-xl p-3 text-xs leading-relaxed
                    ${result.risk.includes('위험') ? 'alert-danger' : result.risk.includes('주의') ? 'alert-warning' : 'alert-success'}`}>
                    💡 {result.insight}
                  </div>
                )}

                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-xs font-bold text-gray-500 mb-2">💰 월 현금흐름</p>
                  <div className={`mb-2 rounded-lg p-2.5 text-xs font-medium ${result.monthly_shortage > 0 ? 'alert-danger' : 'alert-success'}`}>
                    {result.monthly_shortage > 0
                      ? `매달 약 ${result.monthly_shortage}만원이 부족합니다.`
                      : `매달 약 ${Math.abs(result.monthly_shortage)}만원이 남습니다.`}
                  </div>
                  <p className="text-xs text-gray-600 leading-relaxed">{result.cashflow}</p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="border border-gray-100 rounded-xl p-3">
                    <p className="text-xs font-bold text-gray-500 mb-2">수입 vs 지출</p>
                    <ResponsiveContainer width="100%" height={140}>
                      <BarChart data={[
                        { label: '수입', value: profile.income },
                        { label: '지출', value: profile.expense + medical },
                      ]} margin={{ top: 16, right: 8, bottom: 0, left: -20 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false}/>
                        <XAxis dataKey="label" tick={{ fontSize: 11 }}/>
                        <YAxis tick={{ fontSize: 10 }} unit="만"/>
                        <Tooltip formatter={(v: number) => [`${v}만원`]}/>
                        <Bar dataKey="value" radius={[6, 6, 0, 0]}
                          fill={result.monthly_shortage > 0 ? '#EF4444' : '#22C55E'}
                          label={{ position: 'top', fontSize: 10, formatter: (v: number) => `${v}만`}}/>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  {!isElder && (
                    <div className="border border-gray-100 rounded-xl p-3">
                      <p className="text-xs font-bold text-gray-500 mb-2">자산 추이 (30년)</p>
                      {(() => {
                        const maxA = Math.max(...result.assets_over_time, 1)
                        const data = result.assets_over_time.map((v, i) => ({ year: i, asset: v }))
                        return (
                          <ResponsiveContainer width="100%" height={140}>
                            <LineChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -28 }}>
                              <ReferenceArea y1={0} y2={maxA * 0.3} fill="#FEE2E2" fillOpacity={0.4}/>
                              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9"/>
                              <XAxis dataKey="year" unit="년" tick={{ fontSize: 10 }} ticks={[0, 10, 20, 30]}/>
                              <YAxis tick={{ fontSize: 9 }} tickFormatter={v => `${(v/10000).toFixed(0)}억`}/>
                              <Tooltip formatter={(v: number) => [v >= 10000 ? `${(v/10000).toFixed(1)}억` : `${v}만`, '자산']}/>
                              <Legend wrapperStyle={{ fontSize: 10 }}/>
                              {result.sustain_years && result.sustain_years <= 30 && (
                                <ReferenceLine x={result.sustain_years} stroke="#DC2626" strokeDasharray="4 4"
                                  label={{ value: `소진 ${result.sustain_years}년`, position: 'top', fontSize: 9, fill: '#DC2626' }}/>
                              )}
                              <Line type="monotone" dataKey="asset" stroke="#0891B2" strokeWidth={2}
                                dot={false} name="예상 자산"/>
                            </LineChart>
                          </ResponsiveContainer>
                        )
                      })()}
                    </div>
                  )}
                </div>

                <div className="border border-gray-100 rounded-xl p-4">
                  <p className="text-xs font-bold text-gray-500 mb-3">🔮 미래 예측</p>
                  {isElder ? (
                    <div className="space-y-2">
                      {TABS.map((t, i) => (
                        <div key={t}>
                          <p className="text-xs font-bold text-gray-400 mb-1">{t}</p>
                          <div className={`whitespace-pre-wrap text-sm p-2.5 rounded-lg ${i === 0 ? 'alert-info' : i === 1 ? 'alert-warning' : 'alert-danger'}`}>
                            {tabContent[i]}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <>
                      <div className="flex gap-1 mb-2">
                        {TABS.map((t, i) => (
                          <button key={t} onClick={() => setTab(i)}
                            className={`flex-1 py-1.5 rounded-lg text-xs font-medium transition-all ${tab === i ? 'bg-cyan-600 text-white' : 'bg-gray-100 text-gray-600'}`}>
                            {t}
                          </button>
                        ))}
                      </div>
                      <div className={`whitespace-pre-wrap text-sm p-2.5 rounded-lg ${tab === 0 ? 'alert-info' : tab === 1 ? 'alert-warning' : 'alert-danger'}`}>
                        {tabContent[tab]}
                      </div>
                    </>
                  )}
                </div>

                {result.actions && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">{isElder ? '✅ 지금 해야 할 것' : '🎯 AI 추천 행동'}</p>
                    <div className="alert-success whitespace-pre-wrap text-sm">{result.actions}</div>
                  </div>
                )}

                {!isElder && result.easy && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">💬 쉽게 말하면</p>
                    <p className="text-xs text-gray-600 leading-relaxed">{result.easy}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Tip bar */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-cyan-100 rounded-full flex items-center justify-center text-lg flex-shrink-0">💡</div>
            <div>
              <p className="text-sm font-semibold text-gray-800">시뮬레이션 팁</p>
              <p className="text-xs text-gray-500">단 '지금으로서' 기준으로 수입·지출·자산 정보를 최신으로 입력하면 더 정확한 예측을 받을 수 있습니다.</p>
            </div>
          </div>
          <button className="flex items-center gap-1 text-xs text-cyan-600 font-medium hover:underline flex-shrink-0 ml-4">
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

