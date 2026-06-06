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
        className="w-full flex items-center justify-between text-left"
      >
        <span className="font-semibold text-gray-800">👤 내 프로필 설정</span>
        <span className="text-gray-400 text-sm">{open ? '▲ 닫기' : '▼ 열기'}</span>
      </button>

      {open && (
        <div className="mt-4 space-y-4">
          {isBeginner && (
            <div className="bg-blue-50 border border-blue-200 rounded-xl px-4 py-3 text-sm text-blue-700">
              💡 각 항목 옆의 <strong>?</strong> 버튼을 누르면 설명을 볼 수 있어요.
            </div>
          )}
          <div>
            <label className="label">사용자 유형</label>
            <select
              className="input-field"
              value={form.user_type}
              onChange={e => setForm(f => ({ ...f, user_type: e.target.value }))}
            >
              {['고령층', '일반 사용자', '금융 초보자'].map(t => (
                <option key={t}>{t}</option>
              ))}
            </select>
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
            <button onClick={handleSave} className="btn-primary text-sm py-2">
              💾 저장
            </button>
            {saved && <span className="text-green-600 text-sm font-medium">저장되었습니다!</span>}
          </div>
        </div>
      )}
    </div>
  )
}
