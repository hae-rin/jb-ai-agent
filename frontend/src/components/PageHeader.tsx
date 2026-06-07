import { useNavigate } from 'react-router-dom'

interface Props {
  icon: string
  title: string
  subtitle: string
  gradient: string
}

export default function PageHeader({ icon, title, subtitle, gradient }: Props) {
  const nav = useNavigate()
  return (
    <div className={`${gradient} w-full`}>
      <div className="max-w-6xl mx-auto px-6 py-8">
        <button
          onClick={() => nav('/')}
          className="text-white/70 hover:text-white text-sm mb-4 flex items-center gap-1.5 transition-colors"
        >
          <svg viewBox="0 0 16 16" fill="none" className="w-4 h-4">
            <path d="M10 3L5 8l5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          홈으로
        </button>
        <div className="flex items-center gap-4">
          <span className="text-4xl">{icon}</span>
          <div>
            <h1 className="text-2xl font-extrabold text-white leading-tight">{title}</h1>
            <p className="text-white/80 text-sm mt-1">{subtitle}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
