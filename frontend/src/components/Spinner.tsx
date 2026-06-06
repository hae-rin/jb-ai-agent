export default function Spinner({ text = 'AI가 분석 중입니다...' }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16">
      <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
      <p className="text-gray-500 text-sm animate-pulse">{text}</p>
    </div>
  )
}
