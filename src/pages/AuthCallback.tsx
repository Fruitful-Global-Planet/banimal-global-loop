import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'

export default function AuthCallback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { setUser } = useAuth()

  useEffect(() => {
    const fetchSessionAndRedirect = async () => {
      try {
        const res = await fetch('/auth/session', { credentials: 'include' })
        const data = await res.json()
        if (data.user) {
          setUser(data.user)
          // Show toast: Welcome {name}!
          console.log(`Welcome, ${data.user.name}!`)
        }
      } catch (e) {
        console.error('Failed to fetch session:', e)
      } finally {
        // Redirect home after a short delay
        setTimeout(() => navigate('/'), 500)
      }
    }

    if (searchParams.get('auth') === 'success') {
      fetchSessionAndRedirect()
    } else {
      navigate('/')
    }
  }, [searchParams, navigate, setUser])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4" />
        <p className="text-gray-600">Signing you in...</p>
      </div>
    </div>
  )
}
