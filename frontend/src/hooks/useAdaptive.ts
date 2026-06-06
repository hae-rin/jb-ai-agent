import { useProfile } from '../context/ProfileContext'

export function useAdaptive() {
  const { profile } = useProfile()
  const t = profile.user_type
  return {
    isElder:   t === '고령층',
    isBeginner: t === '금융 초보자',
    isNormal:  t === '일반 사용자',
  }
}
