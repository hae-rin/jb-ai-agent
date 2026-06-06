import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { useProfile } from '../context/ProfileContext'

interface BucketItem { name: string; cost: number; years: number }
interface ItemResult extends BucketItem { status: '달성 가능' | '노력 필요' | '어려움' }
interface Result {
  overall: string; analysis: string; priority: string; plan: string; cheer: string
  item_results: ItemResult[]
}

const TRAVEL_EXAMPLE: BucketItem[] = [
  { name: '일본 교토 여행', cost: 300, years: 1 },
  { name: '유럽 여행',      cost: 800, years: 3 },
  { name: '제주 여행',      cost: 200, years: 2 },
  { name: '',               cost: 0,   years: 1 },
  { name: '',               cost: 0,   years: 1 },
]
const FAMILY_EXAMPLE: BucketItem[] = [
  { name: '손자 결혼 축의금',       cost: 1000, years: 5 },
  { name: '봉사활동',              cost: 300,  years: 1 },
  { name: '불우이웃 기부',          cost: 100,  years: 1 },
  { name: '',                      cost: 0,    years: 1 },
  { name: '',                      cost: 0,    years: 1 },
]

const STATUS_COLOR: Record<string, string> = {
  '달성 가능': '#22C55E',
  '노력 필요': '#F59E0B',
  '어려움':    '#EF4444',
}

const STATUS_BG: Record<string, string> = {
  '달성 가능': 'bg-green-100 text-green-700',
  '노력 필요': 'bg-amber-100 text-amber-700',
  '어려움':    'bg-red-100 text-red-700',
}

function HeroRobot() {
  return (
    <svg viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-44 h-52 drop-shadow-lg">
      <circle cx="100" cy="160" r="85" fill="#FEF9C3" opacity="0.6"/>
      <ellipse cx="100" cy="226" rx="38" ry="7" fill="#CBD5E1" opacity="0.25"/>
      <rect x="78" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="105" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="58" y="122" width="84" height="78" rx="22" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M142 130 Q162 118 168 108 Q172 100 165 96 Q158 92 153 102 Q148 112 142 120" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="22" y="134" width="36" height="18" rx="9" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M86 142 L100 133 L114 142 L114 157 Q100 167 86 157 Z" fill="#D97706"/>
      <path d="M94 151 L99 156 L111 144" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <rect x="61" y="57" width="78" height="71" rx="24" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="70" y="69" width="60" height="42" rx="12" fill="#0F172A"/>
      <circle cx="88"  cy="87" r="6.5" fill="#FCD34D"/>
      <circle cx="88"  cy="87" r="3.2" fill="#F59E0B"/>
      <circle cx="112" cy="87" r="6.5" fill="#FCD34D"/>
      <circle cx="112" cy="87" r="3.2" fill="#F59E0B"/>
      <circle cx="86"  cy="85" r="1.8" fill="white" opacity="0.6"/>
      <circle cx="110" cy="85" r="1.8" fill="white" opacity="0.6"/>
      <path d="M84 105 Q100 114 116 105" stroke="#FCD34D" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
      <line x1="100" y1="57" x2="100" y2="40" stroke="#94A3B8" strokeWidth="2.5" strokeLinecap="round"/>
      <circle cx="100" cy="35" r="6" fill="#D97706"/>
      <circle cx="100" cy="35" r="3" fill="#FDE68A"/>
    </svg>
  )
}

export default function BucketList() {
  const { profile } = useProfile()
  const [items, setItems] = useState<BucketItem[]>(
    Array.from({ length: 5 }, () => ({ name: '', cost: 0, years: 1 }))
  )
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')

  const setItem = (i: number, k: keyof BucketItem, v: string | number) =>
    setItems(prev => prev.map((item, idx) => idx === i ? { ...item, [k]: v } : item))

  const analyze = async () => {
    const active = items.filter(it => it.name.trim())
    if (!active.length) return
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await fetch('/api/bucket-list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: profile.age, income: profile.income,
          asset: profile.asset, expense: profile.expense,
          items: active,
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

  const monthlySavings = profile.income - profile.expense

  return (
    <div className="min-h-screen">

      {/* Hero */}
      <div className="bg-gradient-to-br from-[#FFFBEB] via-[#FEF3C7] to-[#FFF8E1] px-8 py-10">
        <div className="max-w-4xl flex items-center justify-between gap-6">
          <div>
            <h1 className="text-3xl font-black text-[#78350F] mb-2 leading-tight">노후 버킷리스트</h1>
            <p className="text-amber-700 text-sm leading-relaxed">
              살면서 꼭 이루고 싶은 꿈들을<br/>AI가 실현 가능한 재무 계획으로 만들어드립니다
            </p>
          </div>
          <div className="relative flex-shrink-0 mr-4">
            <HeroRobot />
            {/* 별 / 꽃 */}
            <div className="absolute -top-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-16 h-14 flex items-center justify-center animate-float-2">
              <svg viewBox="0 0 32 32" fill="none" className="w-9 h-9">
                <path d="M16 4 L19 12 L28 12 L21 18 L24 26 L16 21 L8 26 L11 18 L4 12 L13 12 Z"
                  fill="#FCD34D" stroke="#F59E0B" strokeWidth="1.5" strokeLinejoin="round"/>
              </svg>
            </div>
            {/* 돼지 저금통 */}
            <div className="absolute top-[38%] -right-2 w-11 h-11 bg-amber-400 rounded-xl flex items-center justify-center shadow-lg animate-float-3">
              <svg viewBox="0 0 20 20" fill="none" className="w-6 h-6">
                <ellipse cx="10" cy="11" rx="7" ry="6" fill="white" opacity="0.9"/>
                <circle cx="13" cy="9" r="1" fill="#F59E0B"/>
                <path d="M3 10 Q1 9 1 11 Q1 13 3 12" stroke="white" strokeWidth="1.2" fill="none" strokeLinecap="round"/>
                <path d="M8 5 Q10 3 12 5" stroke="white" strokeWidth="1.2" fill="none" strokeLinecap="round"/>
                <line x1="8" y1="17" x2="8" y2="19" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
                <line x1="12" y1="17" x2="12" y2="19" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </div>
            {/* 체크리스트 */}
            <div className="absolute -bottom-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-14 h-12 flex items-center justify-center animate-float-4">
              <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
                <rect x="4" y="4" width="24" height="24" rx="5" stroke="#F59E0B" strokeWidth="2"/>
                <path d="M10 16 L14 20 L22 12" stroke="#F59E0B" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
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
              <span className="text-amber-500 text-lg">⭐</span>
              <h2 className="font-bold text-gray-800 text-base">꿈 목록 입력</h2>
            </div>

            <div className="space-y-4 mb-6">
              {[
                { bg: 'bg-amber-100',   icon: '🎯', title: '꿈 실현 가능성', desc: '재무 상황 기반으로 각 꿈의 달성 가능성 분석' },
                { bg: 'bg-orange-100',  icon: '📅', title: '단계별 재무 계획', desc: '꿈을 이루기 위한 월별·연도별 저축 계획 수립' },
                { bg: 'bg-yellow-100',  icon: '💌', title: '응원 메시지',      desc: 'AI가 보내는 따뜻한 격려와 실천 조언' },
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

            {/* 월 가용 저축액 배분 */}
            <div className={`rounded-xl p-3 text-xs font-medium mb-4 ${
              monthlySavings > 0 ? 'alert-success' : monthlySavings < 0 ? 'alert-danger' : 'alert-info'
            }`}>
              {monthlySavings > 0
                ? `✅ 매달 약 ${monthlySavings}만원씩 저축할 수 있습니다.`
                : monthlySavings < 0
                ? `⚠️ 매달 약 ${Math.abs(monthlySavings)}만원이 부족합니다.`
                : '수입과 지출이 딱 맞습니다.'}
            </div>

            {/* 예시 버튼 */}
            <div className="flex gap-2 mb-4">
              <button onClick={() => setItems(TRAVEL_EXAMPLE)}
                className="flex-1 text-xs py-2 rounded-xl border border-gray-200 hover:bg-amber-50 hover:border-amber-300 transition-colors">
                🌏 여행 중심 예시
              </button>
              <button onClick={() => setItems(FAMILY_EXAMPLE)}
                className="flex-1 text-xs py-2 rounded-xl border border-gray-200 hover:bg-amber-50 hover:border-amber-300 transition-colors">
                👨‍👩‍👧‍👦 가족 중심 예시
              </button>
            </div>

            {/* 입력 테이블 */}
            <div className="grid grid-cols-[2fr_1fr_1fr] gap-2 mb-2">
              <p className="text-xs text-gray-400 font-medium">꿈 내용</p>
              <p className="text-xs text-gray-400 font-medium">비용(만원)</p>
              <p className="text-xs text-gray-400 font-medium">목표(년)</p>
            </div>
            {items.map((item, i) => (
              <div key={i} className="grid grid-cols-[2fr_1fr_1fr] gap-2 mb-2">
                <input className="input-field text-sm" placeholder={`꿈 ${i + 1}`}
                  value={item.name} onChange={e => setItem(i, 'name', e.target.value)} />
                <input type="number" min={0} step={10} className="input-field text-sm"
                  value={item.cost} onChange={e => setItem(i, 'cost', Number(e.target.value))} />
                <input type="number" min={1} max={30} className="input-field text-sm"
                  value={item.years} onChange={e => setItem(i, 'years', Number(e.target.value))} />
              </div>
            ))}

            <button onClick={analyze} disabled={loading || !items.some(it => it.name.trim())}
              className="w-full mt-4 bg-amber-500 hover:bg-amber-600 active:bg-amber-700 text-white
                         rounded-xl py-3.5 font-bold text-sm transition-all
                         disabled:opacity-60 disabled:cursor-not-allowed
                         flex flex-col items-center gap-0.5">
              <span>✨ AI 재무 계획 만들기</span>
              <span className="text-xs font-normal text-amber-100">꿈을 현실로 만드는 계획을 세워드립니다</span>
            </button>
          </div>

          {/* RIGHT */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="text-lg">📊</span>
              <h2 className="font-bold text-gray-800 text-base">AI 재무 계획</h2>
            </div>

            {loading && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-12 h-12 border-4 border-amber-100 border-t-amber-500 rounded-full animate-spin mb-4"/>
                <p className="text-gray-600 font-medium text-sm">AI가 맞춤 재무 계획을 만들고 있습니다...</p>
                <p className="text-gray-400 text-xs mt-1">꿈 분석 → 재무 매칭 → 계획 수립</p>
              </div>
            )}

            {error && <div className="alert-danger text-sm">{error}</div>}

            {!result && !loading && (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <div className="w-20 h-20 bg-amber-50 rounded-full flex items-center justify-center mb-4">
                  <svg viewBox="0 0 40 40" fill="none" className="w-10 h-10">
                    <path d="M20 6 L23 15 L33 15 L25 21 L28 30 L20 24 L12 30 L15 21 L7 15 L17 15 Z"
                      fill="#FCD34D" stroke="#F59E0B" strokeWidth="1.5" strokeLinejoin="round"/>
                  </svg>
                </div>
                <p className="font-semibold text-gray-600 text-sm mb-1">아직 계획이 없습니다</p>
                <p className="text-xs text-gray-400 leading-relaxed">왼쪽에 이루고 싶은 꿈을 입력하고<br/>AI 재무 계획을 받아보세요</p>
              </div>
            )}

            {result && (
              <div className="space-y-4 overflow-y-auto max-h-[600px] pr-1">
                <div className="border border-amber-100 bg-amber-50 rounded-xl p-3">
                  <p className="text-xs font-bold text-amber-700 mb-1">💛 종합 분석</p>
                  <p className="text-xs text-amber-900 leading-relaxed">{result.overall}</p>
                </div>

                {result.item_results.length > 0 && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-3">🌟 꿈 실현 타임라인</p>
                    <ResponsiveContainer width="100%" height={Math.max(120, result.item_results.length * 42 + 40)}>
                      <BarChart data={result.item_results} layout="vertical"
                        margin={{ top: 0, right: 80, bottom: 0, left: 8 }}>
                        <CartesianGrid strokeDasharray="3 3" horizontal={false}/>
                        <XAxis type="number" unit="년" tick={{ fontSize: 11 }}/>
                        <YAxis type="category" dataKey="name" width={90} tick={{ fontSize: 11 }}/>
                        <Tooltip formatter={(v: number, _: string, entry: any) =>
                          [`${v}년 | ${entry.payload.cost}만원 | ${entry.payload.status}`, '']}/>
                        <Bar dataKey="years" radius={[0, 5, 5, 0]}>
                          {result.item_results.map((entry, i) => (
                            <Cell key={i} fill={STATUS_COLOR[entry.status] ?? '#6B7280'}/>
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="flex gap-4 mt-2">
                      {Object.entries(STATUS_COLOR).map(([label, color]) => (
                        <span key={label} className="flex items-center gap-1 text-xs text-gray-500">
                          <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ background: color }}/>
                          {label}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {result.item_results.length > 0 && (
                  <div className="grid grid-cols-1 gap-2">
                    {result.item_results.map((item, i) => (
                      <div key={i} className="flex items-center justify-between border border-gray-100 rounded-xl px-3 py-2.5">
                        <div>
                          <p className="text-xs font-semibold text-gray-800">{item.name}</p>
                          <p className="text-xs text-gray-400">{item.cost}만원 · {item.years}년 목표</p>
                        </div>
                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${STATUS_BG[item.status]}`}>
                          {item.status}
                        </span>
                      </div>
                    ))}
                  </div>
                )}

                {result.analysis && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">🔍 꿈별 상세 분석</p>
                    <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">{result.analysis}</p>
                  </div>
                )}

                {result.priority && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">📅 추천 순서</p>
                    <div className="alert-success whitespace-pre-wrap text-sm">{result.priority}</div>
                  </div>
                )}

                {result.plan && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <p className="text-xs font-bold text-gray-500 mb-2">💰 월별 계획</p>
                    <div className="alert-success whitespace-pre-wrap text-sm">{result.plan}</div>
                  </div>
                )}

                {result.cheer && (
                  <div className="border border-amber-100 bg-amber-50 rounded-xl p-4">
                    <p className="text-xs font-bold text-amber-700 mb-2">💌 응원 메시지</p>
                    <p className="text-sm text-amber-900 leading-relaxed whitespace-pre-wrap">{result.cheer}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Tip bar */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center text-lg flex-shrink-0">💡</div>
            <div>
              <p className="text-sm font-semibold text-gray-800">버킷리스트 팁</p>
              <p className="text-xs text-gray-500">비용과 목표 시기를 구체적으로 입력할수록 더 현실적인 재무 계획을 받을 수 있습니다.</p>
            </div>
          </div>
          <button className="flex items-center gap-1 text-xs text-amber-600 font-medium hover:underline flex-shrink-0 ml-4">
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

