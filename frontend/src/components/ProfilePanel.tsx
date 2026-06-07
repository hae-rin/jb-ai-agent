import { useState } from 'react'
import { useProfile } from '../context/ProfileContext'
import { useAdaptive } from '../hooks/useAdaptive'

const FIELDS = [
  {
    key: 'age',     label: '나이',
    tip: '현재 만 나이를 입력하세요.',
  },
  {
    key: 'income',  label: '월 소득/연금 (만원)',
    tip: '매달 받는 월급, 연금, 이자 등 모든 수입을 합쳐서 입력하세요.',
  },
  {
    key: 'asset',   label: '금융 자산 (만원)',
    tip: '은행 통장, 적금, 주식, 펀드 등 현금으로 바꿀 수 있는 자산의 합계입니다.',
  },
  {
    key: 'expense', label: '월 생활비 (만원)',
    tip: '식비, 교통비, 공과금, 의료비 등 한 달에 쓰는 돈의 합계입니다.',
  },
] as const

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

type FormState = Record<string, string>

export default function ProfilePanel() {
  const { profile, saveProfile } = useProfile()
  const { isBeginner } = useAdaptive()
  const [saved, setSaved] = useState(false)
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState<FormState>({
    age:      String(profile.age),
    income:   String(profile.income),
    asset:    String(profile.asset),
    expense:  String(profile.expense),
    user_type: profile.user_type,
  })

  const handleToggle = () => {
    if (!open) {
      setForm({
        age:      String(profile.age),
        income:   String(profile.income),
        asset:    String(profile.asset),
        expense:  String(profile.expense),
        user_type: profile.user_type,
      })
    }
    setOpen(o => !o)
  }

  const handleSave = async () => {
    await saveProfile({
      age:      Number(form.age)     || 0,
      income:   Number(form.income)  || 0,
      asset:    Number(form.asset)   || 0,
      expense:  Number(form.expense) || 0,
      user_type: form.user_type,
    })
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="card mb-6">
      <button
        onClick={handleToggle}
        className="flex items-center gap-0.5 text-left"
      >
        <span className="font-semibold text-gray-800">👤 내 프로필 설정</span>
        <svg viewBox="0 0 16 16" fill="none" className={`w-4 h-4 text-gray-400 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}>
          <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {open && (
        <div className="mt-4 space-y-4">
          <div>
            <label className="label">사용자 유형</label>
            <div className="relative inline-flex">
              <select
                className="input-field appearance-none !w-auto pr-8 cursor-pointer"
                value={form.user_type}
                onChange={e => setForm(f => ({ ...f, user_type: e.target.value }))}
              >
                {['고령층', '일반 사용자', '금융 초보자'].map(t => (
                  <option key={t}>{t}</option>
                ))}
              </select>
              <span className="pointer-events-none absolute inset-y-0 right-3 flex items-center text-gray-400">
                <svg viewBox="0 0 16 16" fill="none" className="w-3.5 h-3.5">
                  <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {FIELDS.map(({ key, label, tip }) => (
              <div key={key}>
                <label className="label">
                  {label}
                  {isBeginner && <Tip text={tip} />}
                </label>
                <input
                  type="text"
                  inputMode="numeric"
                  className="input-field"
                  value={form[key]}
                  onChange={e => setForm(f => ({ ...f, [key]: e.target.value.replace(/[^0-9]/g, '') }))}
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
              저장
            </button>
            {saved && <span className="text-green-600 text-sm font-medium">저장되었습니다!</span>}
          </div>
        </div>
      )}
    </div>
  )
}
