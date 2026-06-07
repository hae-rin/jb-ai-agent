import { useNavigate } from 'react-router-dom'
import { useProfile } from '../context/ProfileContext'
import { useAdaptive } from '../hooks/useAdaptive'
import { useState } from 'react'

// ── SVG Icons ─────────────────────────────────────────────────────
function IconAgent() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-10 h-10">
      <rect x="6" y="11" width="20" height="15" rx="5" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="9" y="14" width="14" height="8" rx="2.5" fill="#0F172A"/>
      <circle cx="13" cy="18" r="2" fill="#38BDF8"/>
      <circle cx="13" cy="18" r="1" fill="#0EA5E9"/>
      <circle cx="19" cy="18" r="2" fill="#38BDF8"/>
      <circle cx="19" cy="18" r="1" fill="#0EA5E9"/>
      <circle cx="11.5" cy="16.5" r="0.7" fill="white" opacity="0.7"/>
      <circle cx="17.5" cy="16.5" r="0.7" fill="white" opacity="0.7"/>
      <line x1="16" y1="11" x2="16" y2="7" stroke="#94A3B8" strokeWidth="1.5" strokeLinecap="round"/>
      <circle cx="16" cy="6" r="2" fill="#2563EB"/>
      <circle cx="16" cy="6" r="1" fill="#93C5FD"/>
      <rect x="3" y="13.5" width="3" height="5" rx="1.5" fill="white" stroke="#E2E8F0" strokeWidth="1.2"/>
      <rect x="26" y="13.5" width="3" height="5" rx="1.5" fill="white" stroke="#E2E8F0" strokeWidth="1.2"/>
    </svg>
  )
}
function IconSim() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
      <rect x="4"  y="18" width="6" height="10" rx="1.5" fill="#0891B2"/>
      <rect x="13" y="12" width="6" height="16" rx="1.5" fill="#0891B2"/>
      <rect x="22" y="6"  width="6" height="22" rx="1.5" fill="#0891B2"/>
    </svg>
  )
}
function IconBucket() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
      <polygon points="16,3 19.5,12 29,12 21.5,18 24,27 16,21.5 8,27 10.5,18 3,12 12.5,12" fill="#FDE68A" stroke="#D97706" strokeWidth="1.5" strokeLinejoin="round"/>
    </svg>
  )
}
function IconPhishing() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
      <path d="M16 3 L29 27 H3 Z" fill="#FEE2E2" stroke="#EF4444" strokeWidth="1.5" strokeLinejoin="round"/>
      <rect x="14.5" y="12" width="3" height="8" rx="1.5" fill="#EF4444"/>
      <circle cx="16" cy="23" r="1.5" fill="#EF4444"/>
    </svg>
  )
}
function IconDoc() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
      <rect x="6" y="2" width="20" height="28" rx="3" fill="#EDE9FE" stroke="#7C3AED" strokeWidth="1.5"/>
      <line x1="10" y1="11" x2="22" y2="11" stroke="#7C3AED" strokeWidth="2" strokeLinecap="round"/>
      <line x1="10" y1="16" x2="22" y2="16" stroke="#7C3AED" strokeWidth="2" strokeLinecap="round"/>
      <line x1="10" y1="21" x2="17" y2="21" stroke="#7C3AED" strokeWidth="2" strokeLinecap="round"/>
    </svg>
  )
}
function IconDiamond() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-8 h-8">
      <path d="M16 28 L3 14 L7 5 H25 L29 14 Z" fill="#D1FAE5" stroke="#059669" strokeWidth="1.5" strokeLinejoin="round"/>
      <line x1="3" y1="14" x2="29" y2="14" stroke="#059669" strokeWidth="1.5"/>
      <path d="M10 5 L8 14 L16 28" stroke="#059669" strokeWidth="1" opacity="0.5"/>
      <path d="M22 5 L24 14 L16 28" stroke="#059669" strokeWidth="1" opacity="0.5"/>
    </svg>
  )
}

// ── Robot Mascot ──────────────────────────────────────────────────
function RobotMascot() {
  return (
    <svg viewBox="0 0 220 290" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full drop-shadow-lg">
      <circle cx="110" cy="185" r="105" fill="#DBEAFE" opacity="0.45"/>
      <circle cx="110" cy="185" r="75"  fill="#EFF6FF" opacity="0.5"/>
      <polygon points="40,200 110,108 180,200" fill="#BFDBFE" opacity="0.35"/>
      <rect x="50" y="165" width="120" height="35" fill="#BFDBFE" opacity="0.3"/>
      <rect x="58"  y="170" width="9" height="30" fill="#93C5FD" opacity="0.4"/>
      <rect x="74"  y="170" width="9" height="30" fill="#93C5FD" opacity="0.4"/>
      <rect x="90"  y="170" width="9" height="30" fill="#93C5FD" opacity="0.4"/>
      <rect x="106" y="170" width="9" height="30" fill="#93C5FD" opacity="0.4"/>
      <rect x="122" y="170" width="9" height="30" fill="#93C5FD" opacity="0.4"/>
      <rect x="138" y="170" width="9" height="30" fill="#93C5FD" opacity="0.4"/>
      <rect x="154" y="170" width="9" height="30" fill="#93C5FD" opacity="0.4"/>
      <ellipse cx="110" cy="254" rx="42" ry="8" fill="#CBD5E1" opacity="0.3"/>
      <rect x="85"  y="218" width="20" height="22" rx="7" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="115" y="218" width="20" height="22" rx="7" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="64" y="138" width="92" height="85" rx="24" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="26" y="150" width="38" height="20" rx="10" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="156" y="150" width="38" height="20" rx="10" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <path d="M92 158 L110 149 L128 158 L128 175 Q110 186 92 175 Z" fill="#2563EB"/>
      <path d="M101 169 L107 175 L120 162" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <rect x="68" y="66" width="84" height="78" rx="26" fill="white" stroke="#E2E8F0" strokeWidth="1.5"/>
      <rect x="77" y="78" width="66" height="46" rx="14" fill="#0F172A"/>
      <circle cx="96"  cy="96" r="7" fill="#38BDF8"/>
      <circle cx="96"  cy="96" r="3.5" fill="#0EA5E9"/>
      <circle cx="124" cy="96" r="7" fill="#38BDF8"/>
      <circle cx="124" cy="96" r="3.5" fill="#0EA5E9"/>
      <circle cx="94"  cy="94" r="2" fill="white" opacity="0.6"/>
      <circle cx="122" cy="94" r="2" fill="white" opacity="0.6"/>
      <path d="M91 114 Q110 124 129 114" stroke="#38BDF8" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
      <line x1="110" y1="66" x2="110" y2="46" stroke="#94A3B8" strokeWidth="3" strokeLinecap="round"/>
      <circle cx="110" cy="41" r="7"  fill="#2563EB"/>
      <circle cx="110" cy="41" r="3.5" fill="#93C5FD"/>
    </svg>
  )
}

function Sparkline() {
  return (
    <svg viewBox="0 0 90 36" className="w-22 h-9">
      <polyline
        points="0,30 12,26 24,22 36,18 48,14 60,10 72,6 90,2"
        fill="none" stroke="#2563EB" strokeWidth="2.2"
        strokeLinecap="round" strokeLinejoin="round"
      />
      <circle cx="90" cy="2" r="3.5" fill="#2563EB"/>
    </svg>
  )
}

// ── Services ──────────────────────────────────────────────────────
const SERVICES = [
  {
    Icon: IconAgent,
    iconBg: 'bg-blue-100',
    color: 'text-blue-600',
    border: 'hover:border-blue-300',
    title: 'AI 종합 케어 에이전트',
    desc: '재무 상태, 거래 위험, 맞춤 케어 플랜까지 AI가 단계별로 분석해드립니다.',
    cta: '에이전트 시작하기 →',
    path: '/care-agent',
  },
  {
    Icon: IconSim,
    iconBg: 'bg-cyan-100',
    color: 'text-cyan-600',
    border: 'hover:border-cyan-300',
    title: '미래 생활 안정 시뮬레이션',
    desc: '자산, 연금, 월 생활비를 기반으로 노후 생활 안정성을 분석합니다.',
    cta: '생활 안정 분석하기 →',
    path: '/simulation',
  },
  {
    Icon: IconBucket,
    iconBg: 'bg-amber-100',
    color: 'text-amber-600',
    border: 'hover:border-amber-300',
    title: '노후 버킷리스트',
    desc: '꼭 이루고 싶은 꿈을 AI가 실현 가능한 재무 계획으로 만들어드립니다.',
    cta: '버킷리스트 시작하기 →',
    path: '/bucket-list',
  },
  {
    Icon: IconPhishing,
    iconBg: 'bg-red-100',
    color: 'text-red-500',
    border: 'hover:border-red-300',
    title: '보이스피싱 즉시 판단',
    desc: '의심스러운 전화나 문자를 붙여넣으면 AI가 바로 사기 여부를 판단해드립니다.',
    cta: '지금 바로 판단하기 →',
    path: '/voice-phishing',
  },
  {
    Icon: IconDoc,
    iconBg: 'bg-violet-100',
    color: 'text-violet-600',
    border: 'hover:border-violet-300',
    title: '문서 쉽게 이해하기',
    desc: '복잡한 보험·대출 문서를 쉬운 말로 핵심만 요약해드립니다.',
    cta: '문서 분석 보기 →',
    path: '/doc-reader',
  },
  {
    Icon: IconDiamond,
    iconBg: 'bg-emerald-100',
    color: 'text-emerald-600',
    border: 'hover:border-emerald-300',
    title: '맞춤 금융 상품 추천',
    desc: '나이, 자산, 목표에 따라 단기·장기·노후 맞춤 상품을 추천해드립니다.',
    cta: '맞춤 상품 추천 →',
    path: '/products',
  },
]

function WhyShield() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-6 h-6">
      <path d="M16 4 L26 8 L26 18 Q26 26 16 29 Q6 26 6 18 L6 8 Z" fill="#BFDBFE" stroke="#2563EB" strokeWidth="1.5" strokeLinejoin="round"/>
      <path d="M12 17 L15 20 L21 14" stroke="#2563EB" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
    </svg>
  )
}
function WhyLock() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-6 h-6">
      <rect x="8" y="15" width="16" height="13" rx="3" fill="#BFDBFE" stroke="#2563EB" strokeWidth="1.5"/>
      <path d="M11 15 L11 11 Q11 6 16 6 Q21 6 21 11 L21 15" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round" fill="none"/>
      <circle cx="16" cy="21" r="2" fill="#2563EB"/>
    </svg>
  )
}
function WhyChart() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-6 h-6">
      <rect x="4"  y="18" width="6" height="10" rx="1.5" fill="#93C5FD"/>
      <rect x="13" y="12" width="6" height="16" rx="1.5" fill="#60A5FA"/>
      <rect x="22" y="6"  width="6" height="22" rx="1.5" fill="#2563EB"/>
    </svg>
  )
}
function WhyStar() {
  return (
    <svg viewBox="0 0 32 32" fill="none" className="w-6 h-6">
      <path d="M16 4 L18 13 L27 16 L18 19 L16 28 L14 19 L5 16 L14 13 Z" fill="#BFDBFE" stroke="#2563EB" strokeWidth="1.5" strokeLinejoin="round"/>
      <circle cx="24" cy="8" r="1.5" fill="#2563EB" opacity="0.6"/>
      <circle cx="8"  cy="24" r="1"   fill="#2563EB" opacity="0.4"/>
    </svg>
  )
}

const WHY = [
  { Icon: WhyShield, bg: 'bg-blue-100', title: '금융 사기 예방',    desc: 'AI가 위험 패턴을 분석하여 금융 사기를 예방합니다.' },
  { Icon: WhyLock,   bg: 'bg-blue-100', title: '개인정보 보호',     desc: '강력한 보안으로 고객님의 정보를 안전하게 보호합니다.' },
  { Icon: WhyChart,  bg: 'bg-blue-100', title: '맞춤 재무 분석',    desc: '내 자산과 생활비를 기반으로 노후 안정성을 분석합니다.' },
  { Icon: WhyStar,   bg: 'bg-blue-100', title: '24시간 AI 케어',    desc: '언제 어디서나 AI가 든든한 금융 동반자가 됩니다.' },
]

// ── Tip tooltip (금융 초보자 전용) ────────────────────────────────
function Tip({ text }: { text: string }) {
  const [show, setShow] = useState(false)
  return (
    <span className="relative inline-block ml-1 align-middle">
      <button
        type="button"
        className="w-5 h-5 rounded-full bg-blue-100 text-blue-600 text-xs font-bold leading-none"
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
        onClick={() => setShow(s => !s)}
      >?</button>
      {show && (
        <span className="absolute left-6 top-0 z-20 bg-slate-800 text-white text-xs rounded-xl px-3 py-2 w-52 leading-relaxed shadow-lg whitespace-normal">
          {text}
        </span>
      )}
    </span>
  )
}

// ── Main ──────────────────────────────────────────────────────────
export default function Home() {
  const nav = useNavigate()
  const { profile, saveProfile } = useProfile()
  const { isElder, isBeginner } = useAdaptive()
  const [profileOpen, setProfileOpen] = useState(false)
  const [saved, setSaved]   = useState(false)
  const [form, setForm]     = useState({
    age:       String(profile.age),
    income:    String(profile.income),
    asset:     String(profile.asset),
    expense:   String(profile.expense),
    user_type: profile.user_type,
  })

  const handleToggle = () => {
    if (!profileOpen) setForm({
      age: String(profile.age), income: String(profile.income),
      asset: String(profile.asset), expense: String(profile.expense),
      user_type: profile.user_type,
    })
    setProfileOpen(o => !o)
  }

  const handleSave = async () => {
    await saveProfile({
      age: Number(form.age) || 0,      income: Number(form.income) || 0,
      asset: Number(form.asset) || 0,  expense: Number(form.expense) || 0,
      user_type: form.user_type,
    })
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className={`min-h-screen bg-white font-sans${isElder ? ' mode-elder' : ''}`}>

      {/* ── Navbar ── */}
      <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-sm">
              <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
                <path d="M10 2L3 5.5v5C3 14.25 6.13 17.9 10 19c3.87-1.1 7-4.75 7-8.5v-5L10 2z" fill="white"/>
                <path d="M7 10l2 2 4-4" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div>
              <span className="text-lg font-black text-blue-700 tracking-tight">Slowfit</span>
              <span className="hidden sm:inline text-xs text-gray-400 ml-2">삶처럼, 금융도 천천히</span>
            </div>
          </div>
          <button
            onClick={handleToggle}
            className="flex items-center gap-1.5 text-sm font-medium text-gray-500
                       hover:text-gray-800 transition-colors px-3 py-1.5 rounded-lg hover:bg-gray-100"
          >
            <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
              <circle cx="10" cy="7" r="3.5" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M3 18c0-4 3.13-6 7-6s7 2 7 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            내 프로필
          </button>
        </div>
      </nav>

      {/* ── Profile drawer ── */}
      {profileOpen && (
        <div className="bg-white border-b border-gray-100 shadow-sm animate-fade-in">
          <div className="max-w-7xl mx-auto px-6 py-5">
            <p className="text-sm font-semibold text-gray-700 mb-3">👤 내 프로필 설정 (전 페이지에서 자동 적용)</p>
            <div className="mb-3">
              <label className="label">사용자 유형</label>
              <div className="relative inline-flex">
                <select
                  className="input-field appearance-none !w-auto pr-8 cursor-pointer"
                  value={form.user_type}
                  onChange={e => setForm(f => ({ ...f, user_type: e.target.value }))}
                >
                  {['고령층', '일반 사용자', '금융 초보자'].map(t => <option key={t}>{t}</option>)}
                </select>
                <span className="pointer-events-none absolute inset-y-0 right-3 flex items-center text-gray-400">
                  <svg viewBox="0 0 16 16" fill="none" className="w-3.5 h-3.5">
                    <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </span>
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
              {([
                ['age',     '나이',              '현재 만 나이를 입력하세요.'],
                ['income',  '월 소득/연금(만원)', '매달 받는 월급, 연금, 이자 등 모든 수입을 합쳐서 입력하세요.'],
                ['asset',   '금융 자산(만원)',    '은행 통장, 적금, 주식, 펀드 등 현금으로 바꿀 수 있는 자산의 합계입니다.'],
                ['expense', '월 생활비(만원)',    '식비, 교통비, 공과금, 의료비 등 한 달에 쓰는 돈의 합계입니다.'],
              ] as [keyof typeof form, string, string][]).map(([k, l, tip]) => (
                <div key={k}>
                  <label className="label">
                    {l}
                    {isBeginner && <Tip text={tip} />}
                  </label>
                  <input
                    type="text" inputMode="numeric" className="input-field"
                    value={form[k]}
                    onChange={e => setForm(f => ({ ...f, [k]: e.target.value.replace(/[^0-9]/g,'') }))}
                  />
                </div>
              ))}
            </div>
            <div className="flex items-center gap-3">
              <button onClick={handleSave} className="btn-primary text-sm py-2 flex items-center gap-1.5">
                <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
                  <rect x="2" y="2" width="12" height="12" rx="2" stroke="white" strokeWidth="1.3"/>
                  <rect x="5" y="2" width="6" height="4" rx="0.5" fill="white" opacity="0.4"/>
                  <rect x="4" y="9" width="8" height="4" rx="1" fill="white" opacity="0.6"/>
                </svg>
                프로필 저장
              </button>
              {saved && <span className="text-green-600 text-sm font-medium">저장되었습니다!</span>}
              <p className="text-gray-400 text-xs ml-auto">저장하면 앱을 껐다 켜도 설정이 유지됩니다.</p>
            </div>
          </div>
        </div>
      )}

      {/* ── Hero ── */}
      <section className="bg-gradient-to-br from-[#EEF4FF] via-[#DBEAFE] to-[#EFF6FF]" style={{ minHeight: '520px' }}>
        <div className="max-w-7xl mx-auto px-6 py-16 flex flex-col lg:flex-row items-center gap-10">

          {/* Left */}
          <div className="flex-[1.4] min-w-0">
            <h1 className={`${isElder ? 'text-6xl' : 'text-5xl'} font-black text-[#1E3A5F] leading-tight mb-5 animate-fade-in-up`}>
              삶처럼,<br/>
              <span className="text-blue-600">금융도 천천히</span>
            </h1>
            <p className={`text-gray-500 ${isElder ? 'text-lg' : 'text-base'} leading-relaxed mb-6 animate-fade-in-up-2`}>
              생활비, 연금, 현금흐름부터 금융사기 위험까지<br/>
              AI가 분석하고 맞춤 케어 플랜을 제안해드립니다.
            </p>
            <div className="flex flex-wrap gap-2.5 mb-8 animate-fade-in-up-3">
              {[
                {
                  label: 'AI 맞춤 분석',
                  icon: (
                    <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4 flex-shrink-0">
                      <circle cx="8" cy="8" r="6.5" stroke="#2563EB" strokeWidth="1.3"/>
                      <line x1="8" y1="8" x2="8" y2="4" stroke="#2563EB" strokeWidth="1.3" strokeLinecap="round"/>
                      <line x1="8" y1="8" x2="11" y2="10" stroke="#2563EB" strokeWidth="1.3" strokeLinecap="round"/>
                      <circle cx="8" cy="8" r="1" fill="#2563EB"/>
                    </svg>
                  ),
                },
                {
                  label: '실시간 위험 감지',
                  icon: (
                    <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4 flex-shrink-0">
                      <path d="M8 2 L13 4.5 L13 9 Q13 13 8 14.5 Q3 13 3 9 L3 4.5 Z" fill="#BFDBFE" stroke="#2563EB" strokeWidth="1.2" strokeLinejoin="round"/>
                      <path d="M6 8.5 L7.5 10 L10.5 7" stroke="#2563EB" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  ),
                },
                {
                  label: '노후 생활 분석',
                  icon: (
                    <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4 flex-shrink-0">
                      <rect x="2"  y="9"  width="3" height="5" rx="0.8" fill="#2563EB"/>
                      <rect x="6.5" y="6" width="3" height="8" rx="0.8" fill="#2563EB"/>
                      <rect x="11" y="3"  width="3" height="11" rx="0.8" fill="#2563EB"/>
                    </svg>
                  ),
                },
              ].map(({ label, icon }) => (
                <span key={label}
                  className={`inline-flex items-center gap-1.5 bg-white/85 backdrop-blur-sm
                             rounded-full px-4 py-2 ${isElder ? 'text-base' : 'text-sm'} text-gray-600 font-medium shadow-sm`}>
                  {icon}{label}
                </span>
              ))}
            </div>
            <button
              onClick={() => nav('/simulation')}
              className={`animate-fade-in-up-4 inline-flex items-center gap-2
                         bg-blue-600 hover:bg-blue-700 active:bg-blue-800
                         text-white font-bold ${isElder ? 'text-xl px-9 py-5' : 'text-base px-7 py-3.5'} rounded-2xl
                         shadow-lg shadow-blue-200 hover:shadow-xl hover:shadow-blue-300
                         transition-all duration-200 hover:-translate-y-0.5`}
            >
              <svg viewBox="0 0 20 20" fill="none" className={isElder ? 'w-7 h-7' : 'w-5 h-5'}>
                <rect x="3" y="11" width="4" height="7" rx="1" fill="white" opacity="0.8"/>
                <rect x="8" y="7"  width="4" height="11" rx="1" fill="white" opacity="0.9"/>
                <rect x="13" y="3" width="4" height="15" rx="1" fill="white"/>
              </svg>
              AI 시뮬레이션 시작하기 →
            </button>
          </div>

          {/* Right — robot + floating cards */}
          <div className="flex-1 relative flex items-center justify-center"
               style={{ minHeight: '420px', minWidth: '340px' }}>

            <div className="relative z-10 w-52 h-64 animate-float">
              <RobotMascot/>
            </div>

            {/* Card 1: 노후 생활 안정성 */}
            <div className="absolute top-4 left-0 bg-white rounded-2xl shadow-lg px-4 py-3 w-48 animate-float-2 z-20">
              <p className="text-xs text-gray-400 font-medium mb-1">노후 생활 안정성</p>
              <p className="text-base font-bold text-blue-600 mb-1.5">안정</p>
              <Sparkline/>
            </div>

            {/* Cards 2+3: 월 생활비 / 연금 */}
            <div className="absolute top-6 right-0 flex flex-col gap-2 animate-float-3 z-20">
              <div className="bg-white rounded-2xl shadow-lg px-4 py-3 w-36">
                <p className="text-xs text-gray-400 font-medium mb-0.5">월 생활비</p>
                <p className="text-sm font-bold text-gray-800">1,250,000원</p>
              </div>
              <div className="bg-white rounded-2xl shadow-lg px-4 py-3 w-36">
                <p className="text-xs text-gray-400 font-medium mb-0.5">연금 수령액</p>
                <p className="text-sm font-bold text-gray-800">1,800,000원</p>
              </div>
            </div>

            {/* Card 4: AI 분석 완료 */}
            <div className="absolute bottom-4 right-2 bg-white rounded-2xl shadow-lg px-4 py-3 w-44 animate-float-4 z-20">
              <div className="flex items-center gap-1.5 mb-1">
                <svg viewBox="0 0 24 24" fill="none" className="w-5 h-5 flex-shrink-0">
                  <rect x="5" y="8" width="14" height="11" rx="3.5" fill="white" stroke="#E2E8F0" strokeWidth="1.2"/>
                  <rect x="7" y="10" width="10" height="6" rx="2" fill="#0F172A"/>
                  <circle cx="9.5" cy="13" r="1.5" fill="#38BDF8"/>
                  <circle cx="9.5" cy="13" r="0.7" fill="#0EA5E9"/>
                  <circle cx="14.5" cy="13" r="1.5" fill="#38BDF8"/>
                  <circle cx="14.5" cy="13" r="0.7" fill="#0EA5E9"/>
                  <line x1="12" y1="8" x2="12" y2="5.5" stroke="#94A3B8" strokeWidth="1.2" strokeLinecap="round"/>
                  <circle cx="12" cy="4.5" r="1.5" fill="#2563EB"/>
                  <rect x="3" y="10.5" width="2" height="3.5" rx="1" fill="white" stroke="#E2E8F0" strokeWidth="1"/>
                  <rect x="19" y="10.5" width="2" height="3.5" rx="1" fill="white" stroke="#E2E8F0" strokeWidth="1"/>
                </svg>
                <p className="text-xs text-gray-400 font-medium">AI 분석 완료</p>
              </div>
              <p className="text-xs font-semibold text-gray-700">노후 자금 안정 구간</p>
              <p className="text-xs text-blue-500 font-medium mt-0.5">72세까지 유지 가능</p>
            </div>

          </div>
        </div>
      </section>

      {/* ── Services ── */}
      <section className="max-w-7xl mx-auto px-6 py-14">
        <h2 className="text-center text-xl font-bold text-gray-800 mb-8">
          <span className="text-gray-300">── </span>주요 서비스<span className="text-gray-300"> ──</span>
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {SERVICES.map(s => (
            <div
              key={s.path}
              onClick={() => nav(s.path)}
              className={`group bg-white rounded-[18px] border-[1.5px] border-gray-200
                          ${s.border} hover:shadow-xl hover:-translate-y-2
                          transition-all duration-200 cursor-pointer ${isElder ? 'p-9' : 'p-7'} text-center`}
            >
              <div className={`${isElder ? 'w-20 h-20' : 'w-16 h-16'} ${s.iconBg} rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm`}>
                <s.Icon/>
              </div>
              <h3 className={`${isElder ? 'text-xl' : 'text-base'} font-bold ${s.color} mb-2 leading-snug`}>{s.title}</h3>
              <p className={`text-gray-500 ${isElder ? 'text-base' : 'text-sm'} leading-relaxed mb-4`}>{s.desc}</p>
              <span className={`${isElder ? 'text-base' : 'text-sm'} font-semibold ${s.color} group-hover:underline`}>{s.cta}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Why ── */}
      <section className="max-w-7xl mx-auto px-6 pb-14">
        <h2 className="text-lg font-bold text-gray-800 mb-4">Slowfit이 특별한 이유</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {WHY.map(w => (
            <div key={w.title} className={`bg-gray-50 rounded-2xl ${isElder ? 'p-6' : 'p-5'} flex gap-3 items-start`}>
              <div className={`${isElder ? 'w-14 h-14' : 'w-11 h-11'} ${w.bg} rounded-full flex items-center justify-center flex-shrink-0`}>
                <w.Icon />
              </div>
              <div>
                <p className={`${isElder ? 'text-base' : 'text-sm'} font-bold text-gray-800 mb-1`}>{w.title}</p>
                <p className={`${isElder ? 'text-sm' : 'text-xs'} text-gray-500 leading-relaxed`}>{w.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-gray-200 py-7 text-center text-xs text-gray-400">
        © 2026 Slowfit. All rights reserved. &nbsp;|&nbsp; JB금융그룹 Fin:AI Challenge
      </footer>

    </div>
  )
}
