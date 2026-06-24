import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Trash2, ShoppingBag } from 'lucide-react'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import BobGoDelivery from '@/components/BobGoDelivery'
import CharitableGiving from '@/components/CharitableGiving'
import { useAuth } from '@/contexts/AuthContext'
import { useCart } from '@/contexts/CartContext'
import SocialAuthModal from '@/components/SocialAuthModal'

const TAX_RATE = 0.15

export default function Checkout() {
  const { user, showAuthModal, openAuth, closeAuth } = useAuth()
  const { items, total: subtotal, removeItem, updateQuantity, count } = useCart()
  const [delivery, setDelivery] = useState<{ service: string; price: number } | null>(null)

  const deliveryFee = delivery?.price || 0
  const total = subtotal + deliveryFee
  const vatIncluded = Math.round((total * TAX_RATE) / (1 + TAX_RATE))

  // Build Paystack metadata line items string
  const lineItems = items
    .map((i) => `${i.name}${i.licenceTier ? ` (${i.licenceTier})` : ''} x${i.quantity}`)
    .join(', ')

  const paystackUrl = `https://paystack.com/pay/banimal-checkout?amount=${Math.round(total * 100)}&metadata=${encodeURIComponent(lineItems)}`

  if (count === 0) {
    return (
      <div className="min-h-screen">
        <Navbar />
        {showAuthModal && <SocialAuthModal onClose={closeAuth} />}
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-24 flex flex-col items-center gap-6 text-center">
          <ShoppingBag className="w-12 h-12 text-bark-700/30" />
          <h1 className="font-serif text-3xl text-bark-800">Your cart is empty</h1>
          <p className="text-bark-700/60">Add some products before checking out.</p>
          <Link to="/shop" className="btn-primary rounded-xl">Browse the shop</Link>
        </div>
        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <Navbar />
      {showAuthModal && <SocialAuthModal onClose={closeAuth} />}

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-24">
        <h1 className="font-serif text-3xl text-bark-800 mb-12">Checkout</h1>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Left: cart items + delivery + auth */}
          <div className="space-y-8">
            {/* Cart line items */}
            <div className="bg-cream-50 rounded-2xl border border-cream-200 divide-y divide-cream-200">
              {items.map((item) => (
                <div key={`${item.id}-${item.licenceTier ?? ''}`} className="flex gap-3 p-4 items-start">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-16 h-16 rounded-xl object-cover bg-cream-100 flex-shrink-0"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-bark-800 truncate">{item.artworkTitle ?? item.name}</p>
                    {item.licenceTier && (
                      <p className="text-xs text-bark-700/60">{item.licenceTier}</p>
                    )}
                    <p className="text-xs text-bark-700/60 mt-0.5">R {item.price.toFixed(2)}</p>
                    {!item.licenceTier && (
                      <div className="flex items-center gap-2 mt-2">
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="w-6 h-6 flex items-center justify-center rounded-full border border-cream-300 text-bark-700 hover:bg-cream-200 transition-colors text-sm"
                          aria-label="Decrease quantity"
                        >
                          −
                        </button>
                        <span className="text-sm font-mono text-bark-800 w-4 text-center">{item.quantity}</span>
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="w-6 h-6 flex items-center justify-center rounded-full border border-cream-300 text-bark-700 hover:bg-cream-200 transition-colors text-sm"
                          aria-label="Increase quantity"
                        >
                          +
                        </button>
                      </div>
                    )}
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <p className="text-sm font-mono text-bark-800">R {(item.price * item.quantity).toFixed(2)}</p>
                    <button
                      onClick={() => removeItem(item.id, item.licenceTier)}
                      className="p-1 text-bark-700/40 hover:text-rose-500 transition-colors"
                      aria-label="Remove item"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {!user && (
              <div className="p-6 bg-cream-50 rounded-2xl border border-cream-300">
                <h3 className="font-serif text-lg text-bark-800 mb-2">Sign in for faster checkout</h3>
                <p className="text-sm text-bark-700/60 mb-4">Save your details and track your orders.</p>
                <button onClick={openAuth} className="btn-primary rounded-xl text-sm">
                  Sign in
                </button>
              </div>
            )}

            {user && (
              <div className="p-4 bg-cream-50 rounded-2xl border border-cream-200 flex items-center gap-3">
                <img src={user.avatar} alt={user.name} className="w-9 h-9 rounded-full object-cover" />
                <div>
                  <p className="text-sm font-medium text-bark-800">{user.name}</p>
                  <p className="text-xs text-bark-700/60">{user.email}</p>
                </div>
              </div>
            )}

            <BobGoDelivery orderValueZAR={subtotal} onSelect={setDelivery} />
          </div>

          {/* Right: order summary */}
          <div>
            <div className="bg-cream-50 rounded-2xl border border-cream-200 p-6 space-y-4 sticky top-20">
              <h3 className="font-serif text-lg text-bark-800">Order summary</h3>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-bark-700/80">Subtotal ({count} item{count !== 1 ? 's' : ''})</span>
                  <span className="font-mono">R {subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-bark-700/80">Delivery</span>
                  <span className="font-mono">{deliveryFee > 0 ? `R ${deliveryFee.toFixed(2)}` : '—'}</span>
                </div>
                <div className="flex justify-between text-bark-700/50">
                  <span>VAT included (15%)</span>
                  <span className="font-mono">R {vatIncluded.toFixed(2)}</span>
                </div>
              </div>

              <div className="border-t border-cream-300 pt-4 flex justify-between font-medium">
                <span className="font-serif text-bark-800">Total</span>
                <span className="font-mono text-bark-800">R {total.toFixed(2)}</span>
              </div>

              <CharitableGiving orderTotalZAR={total} />

              {/* Paystack — opens in new tab if inside iframe, same tab otherwise */}
              <a
                href={paystackUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary w-full justify-center rounded-xl mt-2 text-sm"
                onClick={(e) => {
                  if (window.self === window.top) {
                    e.preventDefault()
                    window.location.href = paystackUrl
                  }
                }}
              >
                Pay with Paystack
              </a>

              <p className="text-xs text-center text-bark-700/40 mt-2">
                Secured by Paystack · Visa, Mastercard, Apple Pay, EFT
              </p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
