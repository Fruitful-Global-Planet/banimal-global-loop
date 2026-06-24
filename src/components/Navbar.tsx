import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ShoppingBag, Menu, X, User } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'
import { useCart } from '@/contexts/CartContext'
import SocialAuthModal from './SocialAuthModal'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const { user, showAuthModal, openAuth, closeAuth, signOut } = useAuth()
  const { count: cartCount } = useCart()
  const navigate = useNavigate()

  return (
    <>
      <nav className="fixed top-0 inset-x-0 z-50 bg-cream-100/95 backdrop-blur-sm border-b border-cream-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14">
            <Link to="/" className="flex items-center gap-2">
              <img src="https://banimal.co.za/assets/logo-oV1EcZZO.png" alt="Banimal" className="h-7" />
            </Link>

            <div className="hidden md:flex items-center gap-8">
              <Link to="/shop" className="text-sm tracking-wide text-bark-800 hover:text-bark-700 transition-colors">Shop</Link>
              <Link to="/about" className="text-sm tracking-wide text-bark-800 hover:text-bark-700 transition-colors">About</Link>
              <a href="/#giving" className="text-sm tracking-wide text-bark-800 hover:text-bark-700 transition-colors">Giving</a>
            </div>

            <div className="flex items-center gap-1 sm:gap-2">
              <button
                onClick={user ? signOut : openAuth}
                className="p-2 rounded-full hover:bg-cream-200 transition-colors"
                aria-label="Account"
              >
                {user ? (
                  <img src={user.avatar} alt={user.name} className="w-6 h-6 rounded-full object-cover" />
                ) : (
                  <User className="w-5 h-5 text-bark-800" />
                )}
              </button>
              <button
                onClick={() => navigate('/checkout')}
                className="relative p-2 rounded-full hover:bg-cream-200 transition-colors"
                aria-label="Cart"
              >
                <ShoppingBag className="w-5 h-5 text-bark-800" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 w-4 h-4 bg-bark-800 text-cream-100 text-xs rounded-full flex items-center justify-center leading-none">
                    {cartCount}
                  </span>
                )}
              </button>
              <button
                className="md:hidden p-2 text-bark-800"
                onClick={() => setOpen(!open)}
                aria-label={open ? 'Close menu' : 'Open menu'}
                aria-expanded={open}
              >
                {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>

        {open && (
          <div className="md:hidden bg-cream-100 border-t border-cream-200 px-4 py-4 space-y-1">
            <Link to="/shop" className="block text-bark-800 text-base tracking-wide py-3 border-b border-cream-200" onClick={() => setOpen(false)}>Shop</Link>
            <Link to="/about" className="block text-bark-800 text-base tracking-wide py-3 border-b border-cream-200" onClick={() => setOpen(false)}>About</Link>
            <a href="/#giving" className="block text-bark-800 text-base tracking-wide py-3 border-b border-cream-200" onClick={() => setOpen(false)}>Giving</a>
            <Link to="/checkout" className="block text-bark-800 text-base tracking-wide py-3" onClick={() => setOpen(false)}>
              Cart {cartCount > 0 && <span className="ml-1 text-xs bg-bark-800 text-cream-100 px-1.5 py-0.5 rounded-full">{cartCount}</span>}
            </Link>
          </div>
        )}
      </nav>

      {showAuthModal && <SocialAuthModal onClose={closeAuth} />}
    </>
  )
}
