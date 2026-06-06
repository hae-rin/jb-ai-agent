import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

export interface Profile {
  age: number
  income: number
  asset: number
  expense: number
  user_type: string
}

const defaults: Profile = { age: 70, income: 80, asset: 20000, expense: 150, user_type: '고령층' }

interface ProfileCtx {
  profile: Profile
  setProfile: (p: Profile) => void
  saveProfile: (p: Profile) => Promise<void>
}

const Ctx = createContext<ProfileCtx>({
  profile: defaults,
  setProfile: () => {},
  saveProfile: async () => {},
})

export function ProfileProvider({ children }: { children: ReactNode }) {
  const [profile, setProfileState] = useState<Profile>(defaults)

  useEffect(() => {
    fetch('/api/profile')
      .then(r => r.json())
      .then(data => setProfileState({ ...defaults, ...data }))
      .catch(() => {})
  }, [])

  const setProfile = (p: Profile) => setProfileState(p)

  const saveProfile = async (p: Profile) => {
    setProfileState(p)
    await fetch('/api/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(p),
    })
  }

  return <Ctx.Provider value={{ profile, setProfile, saveProfile }}>{children}</Ctx.Provider>
}

export const useProfile = () => useContext(Ctx)
