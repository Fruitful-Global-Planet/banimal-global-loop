import { useState } from 'react'
import { X } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

interface AuthModalProps {
  onClose: () => void
}

const PROVIDERS = [
  { id: 'google', name: 'Google', icon: '🔍', color: 'bg-white text-gray-900 border border-gray-300' },
  { id: 'apple', name: 'Apple', icon: '🍎', color: 'bg-black text-white' },
  { id: 'facebook', name: 'Facebook', icon: 'f', color: 'bg-blue-600 text-white' },
  { id: 'github', name: 'GitHub', icon: '⚙️', color: 'bg-gray-800 text-white' },
  { id: 'microsoft', name: 'Microsoft', icon: 'Ⓜ️', color: 'bg-blue-500 text-white' },
  { id: 'twitter', name: 'X', icon: '𝕏', color: 'bg-black text-white' },
  { id: 'instagram', name: 'Instagram', icon: '📷', color: 'bg-gradient-to-r from-purple-400 to-pink-600 text-white' },
  { id: 'tiktok', name: 'TikTok', icon: '♪', color: 'bg-black text-white' },
  { id: 'linkedin', name: 'LinkedIn', icon: 'in', color: 'bg-blue-700 text-white' },
  { id: 'discord', name: 'Discord', icon: '📱', color: 'bg-indigo-600 text-white' },
  { id: 'twitch', name: 'Twitch', icon: '▶️', color: 'bg-purple-600 text-white' },
  { id: 'snapchat', name: 'Snapchat', icon: '👻', color: 'bg-yellow-300 text-black' },
];

export default function AuthModal({ onClose }: AuthModalProps) {
  const { setUser, closeAuth } = useAuth();
  const [mode, setMode] = useState<'providers' | 'email'>('providers');
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleOAuthStart = (provider: string) => {
    window.location.href = `/auth/${provider}/start`;
  };

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isSignUp ? '/auth/email/signup' : '/auth/email/signin';
      const payload = isSignUp ? { email, password, name } : { email, password };

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'include',
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || 'Authentication failed');
      }

      // Fetch session to populate user
      const sessionRes = await fetch('/auth/session', { credentials: 'include' });
      const sessionData = await sessionRes.json();
      if (sessionData.user) {
        setUser(sessionData.user);
      }

      closeAuth();
      // Show toast (you'd integrate with your toast library)
      console.log('Success:', isSignUp ? 'Account created' : 'Signed in');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center bg-black/50">
      <div className="bg-white dark:bg-gray-900 rounded-t-3xl md:rounded-2xl w-full md:w-full md:max-w-md shadow-xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            {mode === 'providers' ? 'Sign in or create account' : isSignUp ? 'Create account' : 'Sign in'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
            aria-label="Close"
          >
            <X className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {mode === 'providers' && (
            <>
              {/* Provider Grid */}
              <div className="grid grid-cols-3 gap-3">
                {PROVIDERS.map((provider) => (
                  <button
                    key={provider.id}
                    onClick={() => handleOAuthStart(provider.id)}
                    className={`p-3 rounded-lg font-medium text-sm transition-all hover:shadow-md active:scale-95 ${provider.color}`}
                    title={provider.name}
                  >
                    <span className="text-lg">{provider.icon}</span>
                    <div className="text-xs mt-1 truncate">{provider.name}</div>
                  </button>
                ))}
              </div>

              {/* Divider */}
              <div className="flex items-center gap-3">
                <div className="flex-1 h-px bg-gray-200 dark:bg-gray-700" />
                <span className="text-sm text-gray-500 dark:text-gray-400">or</span>
                <div className="flex-1 h-px bg-gray-200 dark:bg-gray-700" />
              </div>

              {/* Email Button */}
              <button
                onClick={() => {
                  setMode('email');
                  setIsSignUp(false);
                }}
                className="w-full py-3 px-4 bg-gray-900 dark:bg-white text-white dark:text-black rounded-lg font-medium hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors"
              >
                Continue with email
              </button>

              {/* Guest Link */}
              <button
                onClick={onClose}
                className="w-full py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                Continue as guest
              </button>
            </>
          )}

          {mode === 'email' && (
            <>
              <form onSubmit={handleEmailSubmit} className="space-y-4">
                {isSignUp && (
                  <input
                    type="text"
                    placeholder="Full name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required={isSignUp}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white"
                  />
                )}
                <input
                  type="email"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white"
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={isSignUp ? 8 : 1}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white"
                />
                {error && <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-2 bg-gray-900 dark:bg-white text-white dark:text-black rounded-lg font-medium hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Loading...' : isSignUp ? 'Create account' : 'Sign in'}
                </button>
              </form>

              <button
                onClick={() => setIsSignUp(!isSignUp)}
                className="w-full text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                {isSignUp ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
              </button>

              <button
                onClick={() => {
                  setMode('providers');
                  setError('');
                }}
                className="w-full text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                ← Back to providers
              </button>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-800 text-center text-xs text-gray-500 dark:text-gray-400">
          By continuing you agree to our <a href="/terms" className="underline hover:text-gray-700">Terms</a> and <a href="/privacy" className="underline hover:text-gray-700">Privacy Policy</a>
        </div>
      </div>
    </div>
  );
}
