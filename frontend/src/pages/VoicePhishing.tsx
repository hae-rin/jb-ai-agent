import { useState } from 'react'
import { useProfile } from '../context/ProfileContext'

const EXAMPLES = [
  {
    label: '사기 문자',
    safe: false,
    text: `[국민은행] 고객님 계좌가 이상거래로 인해 일시정지 되었습니다.\n본인확인을 위해 아래 링크를 클릭하여 주민등록번호와 카드번호를 입력해 주세요.\nhttp://kb-safe-verify.xyz/confirm\n미처리시 계좌가 영구 동결됩니다.`,
  },
  {
    label: '사기 전화',
    safe: false,
    text: `검찰청 수사관입니다. 고객님 명의로 대포통장이 개설되어 현재 수사 중에 있습니다.\n지금 즉시 본인 계좌에 있는 돈을 안전계좌로 이체하지 않으면 전 재산이 동결됩니다.\n빨리 가까운 ATM으로 가셔서 010-9999-0000 계좌로 이체해 주세요.\n절대 가족에게 말하지 마세요.`,
  },
  {
    label: '정상 문자',
    safe: true,
    text: `[전북은행] 고객님의 정기예금 만기일이 7일 후(2025-02-01)입니다.\n만기 후 처리방법 선택은 인터넷뱅킹 또는 가까운 영업점을 방문해 주시기 바랍니다.\n문의: 1588-4477 (전북은행 고객센터)`,
  },
]

interface Result {
  verdict: string; risk: string; signals: string; easy: string; actions: string
}

function HeroRobot() {
  return (
    <svg viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-44 h-52 drop-shadow-lg">
      <circle cx="100" cy="160" r="85" fill="#FFE4E6" opacity="0.6"/>
      <ellipse cx="100" cy="226" rx="38" ry="7" fill="#CBD5E1" opacity="0.25"/>
      <rect x="78" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="105" y="197" width="17" height="18" rx="6" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="58" y="122" width="84" height="78" rx="22" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M142 130 Q162 118 168 108 Q172 100 165 96 Q158 92 153 102 Q148 112 142 120" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="22" y="134" width="36" height="18" rx="9" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M86 142 L100 133 L114 142 L114 157 Q100 167 86 157 Z" fill="#DC2626"/>
      <path d="M94 151 L99 156 L111 144" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <rect x="61" y="57" width="78" height="71" rx="24" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="70" y="69" width="60" height="42" rx="12" fill="#0F172A"/>
      <circle cx="88"  cy="87" r="6.5" fill="#FCA5A5"/>
      <circle cx="88"  cy="87" r="3.2" fill="#F87171"/>
      <circle cx="112" cy="87" r="6.5" fill="#FCA5A5"/>
      <circle cx="112" cy="87" r="3.2" fill="#F87171"/>
      <circle cx="86"  cy="85" r="1.8" fill="white" opacity="0.6"/>
      <circle cx="110" cy="85" r="1.8" fill="white" opacity="0.6"/>
      <path d="M84 105 Q100 114 116 105" stroke="#FCA5A5" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
      <line x1="100" y1="57" x2="100" y2="40" stroke="#94A3B8" strokeWidth="2.5" strokeLinecap="round"/>
      <circle cx="100" cy="35" r="6" fill="#DC2626"/>
      <circle cx="100" cy="35" r="3" fill="#FECACA"/>
    </svg>
  )
}

export default function VoicePhishing() {
  const { profile } = useProfile()
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')

  const analyze = async () => {
    if (!content.trim()) return
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await fetch('/api/voice-phishing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, user_type: profile.user_type }),
      })
      if (!r.ok) throw new Error(await r.text())
      setResult(await r.json())
    } catch {
      setError('AI 서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
    } finally {
      setLoading(false)
    }
  }

  const isFraud   = result?.verdict.includes('사기')
  const isCaution = result?.verdict.includes('주의')

  return (
    <div className="min-h-screen">

      {/* Hero */}
      <div className="bg-gradient-to-br from-[#FFF1F2] via-[#FFE4E6] to-[#FFF1F2] px-8 py-10">
        <div className="max-w-4xl flex items-center justify-between gap-6">
          <div>
            <h1 className="text-3xl font-black text-[#7F1D1D] mb-2 leading-tight">보이스피싱<br/>즉시 판단</h1>
            <p className="text-red-700 text-sm leading-relaxed">
              의심스러운 전화·문자를 붙여넣으면<br/>AI가 3초 안에 위기 패턴으로 판단합니다
            </p>
          </div>
          <div className="relative flex-shrink-0 mr-4">
            <HeroRobot />
            <div className="absolute -top-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-16 h-14 flex items-center justify-center animate-float-2">
              <svg viewBox="0 0 32 32" fill="none" className="w-9 h-9">
                <path d="M16 4 L26 8 L26 17 Q26 24 16 28 Q6 24 6 17 L6 8 Z"
                  fill="#FECACA" stroke="#DC2626" strokeWidth="1.8" strokeLinejoin="round"/>
                <path d="M12 16 L15 19 L21 13" stroke="#DC2626" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
              </svg>
            </div>
            <div className="absolute top-[38%] -right-2 w-11 h-11 bg-red-500 rounded-xl flex items-center justify-center shadow-lg animate-float-3">
              <svg viewBox="0 0 20 20" fill="none" className="w-6 h-6">
                <path d="M6 3 Q4 3 3 5 Q2 7 4 10 Q6 13 8 15 Q11 18 14 18 Q16 18 17 16 Q18 15 17 14 L15 12 Q14 11 13 12 L12 13 Q11 14 10 13 Q8 11 7 9 Q6 8 7 7 L8 6 Q9 5 8 4 Z"
                  fill="white" opacity="0.9"/>
                <circle cx="15" cy="5" r="3" fill="#FCA5A5"/>
                <text x="15" y="7" textAnchor="middle" fontSize="4.5" fill="#DC2626" fontWeight="bold">!</text>
              </svg>
            </div>
            <div className="absolute -bottom-2 -right-2 bg-white rounded-2xl shadow-lg p-3 w-14 h-12 flex items-center justify-center animate-float-4">
              <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
                <path d="M16 4 Q22 4 24 10 L25 20 L7 20 L8 10 Q10 4 16 4 Z"
                  fill="#FECACA" stroke="#DC2626" strokeWidth="1.8" strokeLinejoin="round"/>
                <path d="M13 20 Q13 23 16 23 Q19 23 19 20" stroke="#DC2626" strokeWidth="1.8" fill="none" strokeLinecap="round"/>
                <line x1="16" y1="2" x2="16" y2="4" stroke="#DC2626" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Main */}
      <div className="px-8 py-6">
        <div className="flex flex-col gap-5 mb-5">

          {/* LEFT */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
                <path d="M8 2 L14 13 H2 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.2" strokeLinejoin="round"/>
                <rect x="7.3" y="5.5" width="1.4" height="4" rx="0.7" fill="#DC2626"/>
                <circle cx="8" cy="11" r="0.7" fill="#DC2626"/>
              </svg>
              <h2 className="font-bold text-gray-800 text-base">의심 내용 입력</h2>
            </div>

            <div className="space-y-4 mb-6">
              {[
                {
                  bg: 'bg-red-100',
                  icon: (
                    <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
                      <circle cx="9" cy="9" r="5.5" stroke="#DC2626" strokeWidth="1.3"/>
                      <line x1="13" y1="13" x2="17" y2="17" stroke="#DC2626" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                  ),
                  title: '사기 패턴 분석', desc: '알려진 보이스피싱 패턴과 비교 분석',
                },
                {
                  bg: 'bg-orange-100',
                  icon: (
                    <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
                      <path d="M10 2 L18 16 H2 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.3" strokeLinejoin="round"/>
                      <rect x="9.2" y="7" width="1.6" height="5" rx="0.8" fill="#DC2626"/>
                      <circle cx="10" cy="13.5" r="0.9" fill="#DC2626"/>
                    </svg>
                  ),
                  title: '위험 신호 탐지', desc: '긴급성 강요·계좌이체 요구 등 신호 탐지',
                },
                {
                  bg: 'bg-rose-100',
                  icon: (
                    <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
                      <path d="M10 2 L16 5.5 L16 11 Q16 16 10 18 Q4 16 4 11 L4 5.5 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.3" strokeLinejoin="round"/>
                      <path d="M7 10.5 L9 12.5 L13.5 8" stroke="#DC2626" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                    </svg>
                  ),
                  title: '즉시 대응 안내', desc: '위기 상황 시 즉각 취해야 할 행동 안내',
                },
              ].map(f => (
                <div key={f.title} className="flex items-center gap-3">
                  <div className={`w-10 h-10 ${f.bg} rounded-full flex items-center justify-center flex-shrink-0`}>{f.icon}</div>
                  <div>
                    <p className="text-sm font-semibold text-gray-800">{f.title}</p>
                    <p className="text-xs text-gray-400">{f.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            <p className="text-xs text-gray-500 font-medium mb-2">예시 불러오기</p>
            <div className="flex flex-col gap-2 mb-4">
              {EXAMPLES.map(ex => (
                <button key={ex.label} onClick={() => setContent(ex.text)}
                  className={`text-sm px-3 py-2.5 rounded-xl border text-left transition-colors flex items-center gap-2
                    ${ex.safe
                      ? 'border-green-200 hover:bg-green-50 text-green-700'
                      : 'border-red-200 hover:bg-red-50 text-red-700'}`}>
                  {ex.safe
                    ? (
                      <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4 flex-shrink-0">
                        <circle cx="8" cy="8" r="6" fill="#D1FAE5" stroke="#059669" strokeWidth="1.2"/>
                        <path d="M5 8 L7 10 L11 6" stroke="#059669" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    )
                    : (
                      <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4 flex-shrink-0">
                        <path d="M8 2 L14 13 H2 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.2" strokeLinejoin="round"/>
                        <rect x="7.3" y="5.5" width="1.4" height="4" rx="0.7" fill="#DC2626"/>
                        <circle cx="8" cy="11" r="0.7" fill="#DC2626"/>
                      </svg>
                    )}
                  {ex.label}
                </button>
              ))}
            </div>

            <label className="label">의심스러운 내용 직접 입력</label>
            <textarea
              className="input-field resize-none mb-4"
              rows={7}
              placeholder={'예) [국민은행] 고객님 계좌가 정지되었습니다.\n즉시 링크를 클릭해 본인 확인을 해주세요.\nhttp://...'}
              value={content}
              onChange={e => setContent(e.target.value)}
            />

            <button onClick={analyze} disabled={loading || !content.trim()}
              className="w-full bg-red-600 hover:bg-red-700 active:bg-red-800 text-white
                         rounded-xl py-3.5 font-bold text-sm transition-all
                         disabled:opacity-60 disabled:cursor-not-allowed
                         flex flex-col items-center gap-0.5">
              <span className="inline-flex items-center gap-2">
                <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
                  <path d="M10 2 L16 5.5 L16 11 Q16 16 10 18 Q4 16 4 11 L4 5.5 Z" fill="white" opacity="0.2" stroke="white" strokeWidth="1.2" strokeLinejoin="round"/>
                  <path d="M7 10.5 L9 12.5 L13.5 8" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                </svg>
                바로 판단하기
              </span>
              <span className="text-xs font-normal text-red-200">AI가 즉시 위기 패턴으로 분석합니다</span>
            </button>
          </div>

          {/* RIGHT */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div className="flex items-center gap-2 mb-5">
              <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
                <rect x="1" y="9" width="3" height="6" rx="0.8" fill="#DC2626"/>
                <rect x="6" y="6" width="3" height="9" rx="0.8" fill="#DC2626"/>
                <rect x="11" y="3" width="3" height="12" rx="0.8" fill="#DC2626"/>
              </svg>
              <h2 className="font-bold text-gray-800 text-base">판단 결과</h2>
            </div>

            {loading && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-12 h-12 border-4 border-red-100 border-t-red-600 rounded-full animate-spin mb-4"/>
                <p className="text-gray-600 font-medium text-sm">AI가 분석 중입니다...</p>
                <p className="text-gray-400 text-xs mt-1">패턴 매칭 및 위험 신호 탐지 후 판정</p>
              </div>
            )}

            {error && <div className="alert-danger text-sm">{error}</div>}

            {!result && !loading && (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <div className="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mb-4">
                  <svg viewBox="0 0 40 40" fill="none" className="w-10 h-10">
                    <path d="M20 6 L32 11 L32 23 Q32 32 20 37 Q8 32 8 23 L8 11 Z"
                      fill="#FECACA" stroke="#FCA5A5" strokeWidth="1.5"/>
                    <path d="M14 19 L18 23 L26 15" stroke="#EF4444" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                  </svg>
                </div>
                <p className="font-semibold text-gray-600 text-sm mb-1">아직 판단 결과가 없습니다</p>
                <p className="text-xs text-gray-400 leading-relaxed">왼쪽에 의심스러운 내용을 입력하고<br/>판단 버튼을 눌러주세요</p>
              </div>
            )}

            {result && (
              <div className="space-y-4">
                <div className={`rounded-xl p-5 border-2 ${isFraud ? 'border-red-400 bg-red-50' : isCaution ? 'border-amber-400 bg-amber-50' : 'border-green-400 bg-green-50'}`}>
                  <div className={`text-lg font-black mb-1 flex items-center gap-2 ${isFraud ? 'text-red-700' : isCaution ? 'text-amber-700' : 'text-green-700'}`}>
                    {isFraud
                      ? (
                        <>
                          <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5 flex-shrink-0">
                            <path d="M10 2 L18 16 H2 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.3" strokeLinejoin="round"/>
                            <rect x="9.2" y="7" width="1.6" height="5" rx="0.8" fill="#DC2626"/>
                            <circle cx="10" cy="13.5" r="0.9" fill="#DC2626"/>
                          </svg>
                          사기 — 즉시 전화를 끊으세요!
                        </>
                      )
                      : isCaution
                      ? (
                        <>
                          <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5 flex-shrink-0">
                            <path d="M10 2 L18 16 H2 Z" fill="#FEF3C7" stroke="#D97706" strokeWidth="1.3" strokeLinejoin="round"/>
                            <rect x="9.2" y="7" width="1.6" height="5" rx="0.8" fill="#D97706"/>
                            <circle cx="10" cy="13.5" r="0.9" fill="#D97706"/>
                          </svg>
                          주의 — 섣불리 행동하지 마세요
                        </>
                      )
                      : (
                        <>
                          <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5 flex-shrink-0">
                            <circle cx="10" cy="10" r="8" fill="#D1FAE5" stroke="#059669" strokeWidth="1.3"/>
                            <path d="M6.5 10 L8.5 12 L13.5 7" stroke="#059669" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                          </svg>
                          정상으로 보입니다.
                        </>
                      )}
                  </div>
                  <p className={`text-base font-medium ${isFraud ? 'text-red-600' : isCaution ? 'text-amber-600' : 'text-green-600'}`}>
                    위험도: {result.risk}
                  </p>
                </div>

                <div className="border border-gray-100 rounded-xl p-4">
                  <div className="flex items-center gap-1.5 mb-2">
                    <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
                      <circle cx="7" cy="7" r="4.5" stroke="#DC2626" strokeWidth="1.3"/>
                      <line x1="10.5" y1="10.5" x2="14" y2="14" stroke="#DC2626" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    <p className="text-sm font-bold text-gray-500">발견된 위험 신호</p>
                  </div>
                  {result.signals && result.signals !== '이상 없음'
                    ? <div className="alert-danger whitespace-pre-wrap text-base">{result.signals}</div>
                    : <div className="alert-success text-sm">식별된 위험 신호가 없습니다.</div>}
                </div>

                <div className="border border-gray-100 rounded-xl p-4">
                  <div className="flex items-center gap-1.5 mb-2">
                    <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
                      <path d="M2 3 Q2 2 3 2 L13 2 Q14 2 14 3 L14 10 Q14 11 13 11 L6 11 L3 14 L3 11 Q2 11 2 10 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.2"/>
                    </svg>
                    <p className="text-sm font-bold text-gray-500">쉽게 말하면</p>
                  </div>
                  <p className="text-base text-gray-600 leading-relaxed">{result.easy}</p>
                </div>

                {result.actions && (
                  <div className="border border-gray-100 rounded-xl p-4">
                    <div className="flex items-center gap-1.5 mb-2">
                      <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
                        <circle cx="8" cy="8" r="6" fill="#D1FAE5" stroke="#059669" strokeWidth="1.2"/>
                        <path d="M5 8 L7 10 L11 6" stroke="#059669" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      <p className="text-sm font-bold text-gray-500">지금 해야 할 행동</p>
                    </div>
                    <div className={`whitespace-pre-wrap text-base ${isFraud || isCaution ? 'alert-danger' : 'alert-success'}`}>
                      {result.actions}
                    </div>
                  </div>
                )}

                {(isFraud || isCaution) && (
                  <div className="border border-red-100 rounded-xl p-4">
                    <div className="flex items-center gap-1.5 mb-3">
                      <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
                        <path d="M5 2 Q3.5 2 3 4 Q2 6 4 8.5 Q5.5 10.5 7.5 12.5 Q9.5 14.5 11.5 14 Q13 13.5 13 12 L11.5 10.5 Q11 10 10 10.5 L9.5 11 Q9 11.5 8.5 11 Q7 9.5 6.5 8 Q6 7.5 6.5 7 L7 6.5 Q7.5 6 7 5 Z" fill="#DC2626" opacity="0.8"/>
                      </svg>
                      <p className="text-sm font-bold text-red-600">긴급 신고 연락처</p>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      {[['금융감독원', '1332'], ['경찰청', '112'], ['금융범죄신고', '182']].map(([label, tel]) => (
                        <div key={tel} className="alert-danger text-center rounded-xl p-3">
                          <div className="flex items-center justify-center gap-1 mb-1">
                            <svg viewBox="0 0 16 16" fill="none" className="w-3 h-3">
                              <path d="M8 2 L14 13 H2 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.2" strokeLinejoin="round"/>
                              <rect x="7.3" y="5.5" width="1.4" height="4" rx="0.7" fill="#DC2626"/>
                              <circle cx="8" cy="11" r="0.7" fill="#DC2626"/>
                            </svg>
                            <p className="font-bold text-sm">{label}</p>
                          </div>
                          <div className="flex items-center justify-center gap-1">
                            <svg viewBox="0 0 16 16" fill="none" className="w-3.5 h-3.5">
                              <path d="M5 2 Q3.5 2 3 4 Q2 6 4 8.5 Q5.5 10.5 7.5 12.5 Q9.5 14.5 11.5 14 Q13 13.5 13 12 L11.5 10.5 Q11 10 10 10.5 L9.5 11 Q9 11.5 8.5 11 Q7 9.5 6.5 8 Q6 7.5 6.5 7 L7 6.5 Q7.5 6 7 5 Z" fill="#DC2626" opacity="0.8"/>
                            </svg>
                            <p className="text-xl font-black">{tel}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Tip bar */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm px-6 py-4 flex items-center gap-3">
          <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
            <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
              <path d="M10 2 Q14 2 14 6 Q14 9 11 10.5 L11 13 L9 13 L9 10.5 Q6 9 6 6 Q6 2 10 2 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="1.3"/>
              <rect x="9" y="14" width="2" height="2" rx="0.5" fill="#DC2626"/>
              <path d="M7 17 L13 17" stroke="#DC2626" strokeWidth="1.3" strokeLinecap="round"/>
            </svg>
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-800">보이스피싱 예방 팁</p>
            <p className="text-xs text-gray-500">어떤 기관도 전화·문자로 계좌 이체, 개인정보 입력을 요구하지 않습니다. 의심되면 즉시 신고 확인하세요</p>
          </div>
        </div>
      </div>
    </div>
  )
}
