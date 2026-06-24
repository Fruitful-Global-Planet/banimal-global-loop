import { createContext, useContext, useState, type ReactNode } from 'react'

interface User {
  id: string
  name: string
  email: string
  avatar?: string
  provider: string
}

interface AuthCtx {
  user: User | null
  showAuthModal: boolean
  openAuth: () => void
  closeAuth: () => void
  signOut: () => void
  setUser: (u: User | null) => void
}

const Ctx = createContext<AuthCtx | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [showAuthModal, setShowAuthModal] = useState(false)

  const openAuth = () => setShowAuthModal(true)
  const closeAuth = () => setShowAuthModal(false)
  const signOut = () => { setUser(null); localStorage.removeItem('bam_user') }

  return (
    <Ctx.Provider value={{ user, showAuthModal, openAuth, closeAuth, signOut, setUser }}>
      {children}
    </Ctx.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('useAuth must be inside AuthProvider')
  return ctx
}
