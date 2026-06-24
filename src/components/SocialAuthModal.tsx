import { X } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

const PROVIDERS = [
  { id: 'google', label: 'Continue with Google', bg: 'hover:bg-gray-50', icon: '🔵' },
  { id: 'facebook', label: 'Continue with Facebook', bg: 'hover:bg-blue-50', icon: '📘' },
  { id: 'instagram', label: 'Continue with Instagram', bg: 'hover:bg-pink-50', icon: '📸' },
  { id: 'apple', label: 'Continue with Apple', bg: 'hover:bg-gray-100', icon: '🍎' },
  { id: 'microsoft', label: 'Continue with Microsoft', bg: 'hover:bg-blue-50', icon: '🪟' },
  { id: 'github', label: 'Continue with GitHub', bg: 'hover:bg-gray-50', icon: '🐙' },
  { id: 'tiktok', label: 'Continue with TikTok', bg: 'hover:bg-gray-50', icon: '🎵' },
  { id: 'substack', label: 'Continue with Substack', bg: 'hover:bg-orange-50', icon: '📰' },
]

interface Props {
  onClose: () => void
}

export default function SocialAuthModal({ onClose }: Props) {
  const { setUser, closeAuth } = useAuth()

  const handleOAuth = (providerId: string) => {
    // In production: redirect to /api/auth/{provider}/redirect
    // For now, simulate sign-in with mock user
    const mockUser = {
      id: `${providerId}-demo`,
      name: 'Demo User',
      email: `demo@banimal.co.za`,
      avatar: `https://api.dicebear.com/7.x/initials/svg?seed=Demo`,
      provider: providerId,
    }
    setUser(mockUser)
    localStorage.setItem('bam_user', JSON.stringify(mockUser))
    closeAuth()
  }

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-4" role="dialog" aria-modal="true">
      <div className="absolute inset-0 bg-bark-900/40 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-cream-50 w-full max-w-sm rounded-2xl shadow-2xl p-8 animate-slide-up">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1 rounded-full hover:bg-cream-200 transition-colors"
          aria-label="Close"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="text-center mb-8">
          <img src="https://banimal.co.za/assets/logo-oV1EcZZO.png" alt="Banimal" className="h-7 mx-auto mb-4" />
          <h2 className="text-xl font-serif font-semibold text-bark-800">Sign in to Banimal</h2>
          <p className="text-sm text-bark-700/60 mt-1">Join 10,000+ families who love Banimal</p>
        </div>

        <div className="space-y-2">
          {PROVIDERS.map((p) => (
            <button
              key={p.id}
              onClick={() => handleOAuth(p.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 border border-cream-300 rounded-xl text-sm text-bark-800 font-medium transition-colors ${p.bg}`}
            >
              <span className="text-lg">{p.icon}</span>
              <span>{p.label}</span>
            </button>
          ))}
        </div>

        <p className="text-xs text-center text-bark-700/40 mt-6">
          By signing in you agree to our Terms &amp; Privacy Policy
        </p>
      </div>
    </div>
  )
}
