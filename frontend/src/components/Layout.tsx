import { useNavigate, useLocation } from 'react-router-dom'
import { useState } from 'react'
import ProfilePanel from './ProfilePanel'

const NAV = [
  { emoji: '🤖', label: 'AI 종합 케어 에이전트',    path: '/care-agent',     bg: 'bg-blue-100'    },
  { emoji: '📊', label: '미래 생활 안정 시뮬레이션', path: '/simulation',     bg: 'bg-cyan-100'    },
  { emoji: '🌟', label: '노후 버킷리스트',           path: '/bucket-list',    bg: 'bg-amber-100'   },
  { emoji: '🚨', label: '보이스피싱 즉시 판단',      path: '/voice-phishing', bg: 'bg-red-100'     },
  { emoji: '📄', label: '문서 쉽게 이해하기',        path: '/doc-reader',     bg: 'bg-violet-100'  },
  { emoji: '💎', label: '맞춤 금융 상품 추천',       path: '/products',       bg: 'bg-emerald-100' },
]

function ShieldIllustration() {
  return (
    <svg viewBox="0 0 80 88" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-20 h-20">
      <ellipse cx="40" cy="83" rx="24" ry="5" fill="#C7D2FE" opacity="0.5"/>
      <path d="M40 4 L70 17 L70 46 Q70 66 40 80 Q10 66 10 46 L10 17 Z" fill="#3B82F6"/>
      <path d="M40 4 L70 17 L70 46 Q70 66 40 80 Q10 66 10 46 L10 17 Z" fill="white" opacity="0.08"/>
      <path d="M40 11 L63 22 L63 45 Q63 61 40 73 Q17 61 17 45 L17 22 Z" fill="#60A5FA" opacity="0.5"/>
      <path d="M27 44 L36 53 L55 34" stroke="white" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
      <circle cx="58" cy="16" r="4" fill="#BFDBFE" opacity="0.7"/>
      <circle cx="20" cy="58" r="3" fill="#BFDBFE" opacity="0.5"/>
    </svg>
  )
}

export default function Layout({ children }: { children: React.ReactNode }) {
  const nav = useNavigate()
  const loc = useLocation()
  const [profileOpen, setProfileOpen] = useState(false)

  return (
    <div className="min-h-screen bg-[#F0F4FF]">
      {/* ── Top Navbar ── */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-100 z-50 flex items-center px-6 justify-between shadow-sm">
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

        <div className="flex items-center gap-3">
          <button className="w-9 h-9 rounded-full flex items-center justify-center hover:bg-gray-100 transition-colors text-gray-500">
            <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5">
              <path d="M10 2a6 6 0 0 0-6 6v2l-1.5 3h15L16 10V8a6 6 0 0 0-6-6zM8 17a2 2 0 0 0 4 0"
                stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
          </button>
          <button
            onClick={() => setProfileOpen(o => !o)}
            className="flex items-center gap-2 text-sm font-medium text-gray-600
                       border border-gray-200 rounded-full px-4 py-1.5
                       hover:border-blue-300 hover:text-blue-600 transition-colors"
          >
            <svg viewBox="0 0 20 20" fill="none" className="w-4 h-4">
              <circle cx="10" cy="7" r="3.5" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M3 18c0-4 3.13-6 7-6s7 2 7 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            내 프로필
            <svg viewBox="0 0 16 16" fill="none" className={`w-3.5 h-3.5 transition-transform ${profileOpen ? 'rotate-180' : ''}`}>
              <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </header>

      {/* ── Profile dropdown ── */}
      {profileOpen && (
        <div className="fixed top-16 right-0 z-40 w-[420px] bg-white border-b border-l border-gray-100 shadow-lg animate-fade-in">
          <div className="p-5">
            <ProfilePanel />
          </div>
        </div>
      )}

      <div className="flex pt-16">
        {/* ── Sidebar ── */}
        <aside className="fixed left-0 top-16 w-[272px] h-[calc(100vh-4rem)] bg-white border-r border-gray-100 flex flex-col overflow-y-auto">

          {/* Home button */}
          <div className="p-4 pb-2">
            <button
              onClick={() => nav('/')}
              className="w-full flex items-center gap-3 bg-blue-600 hover:bg-blue-700 text-white
                         rounded-xl px-4 py-3 font-semibold text-sm transition-colors"
            >
              <svg viewBox="0 0 20 20" fill="none" className="w-5 h-5 flex-shrink-0">
                <path d="M3 9.5L10 3l7 6.5V17a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z" stroke="white" strokeWidth="1.5"/>
                <rect x="7" y="11" width="6" height="7" rx="1" stroke="white" strokeWidth="1.5"/>
              </svg>
              홈으로
            </button>
          </div>

          {/* Nav items */}
          <nav className="px-3 flex-1">
            {NAV.map(item => {
              const active = loc.pathname === item.path
              return (
                <button
                  key={item.path}
                  onClick={() => nav(item.path)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl mb-0.5 transition-colors text-left ${
                    active
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <div className={`w-8 h-8 ${active ? 'bg-blue-100' : item.bg} rounded-full flex items-center justify-center text-base flex-shrink-0`}>
                    {item.emoji}
                  </div>
                  <span className={`text-sm font-medium leading-snug ${active ? 'font-semibold' : ''}`}>{item.label}</span>
                  {active && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-blue-600"/>}
                </button>
              )
            })}
          </nav>

          {/* Bottom promo card */}
          <div className="p-4 mt-2">
            <div className="relative bg-gradient-to-br from-blue-50 via-indigo-50 to-blue-100 rounded-2xl p-4 overflow-hidden">
              <p className="font-bold text-gray-800 text-sm mb-1">Slowfit과 함께</p>
              <p className="text-xs text-gray-500 leading-relaxed">삶처럼, 금융도 천천히</p>
              <div className="absolute right-0 bottom-0 opacity-90">
                <ShieldIllustration/>
              </div>
            </div>
          </div>
        </aside>

        {/* ── Main content ── */}
        <main className="ml-[272px] flex-1 min-h-[calc(100vh-4rem)]">
          {children}
        </main>
      </div>
    </div>
  )
}
