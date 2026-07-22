import { useState } from 'react'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import BobGoDelivery from '@/components/BobGoDelivery'
import CharitableGiving from '@/components/CharitableGiving'
import { useAuth } from '@/contexts/AuthContext'
import SocialAuthModal from '@/components/SocialAuthModal'

const ORDER_TOTAL = 578
const TAX_RATE = 0.15

export default function Checkout() {
  const { user, showAuthModal, openAuth, closeAuth } = useAuth()
  const [delivery, setDelivery] = useState<{ service: string; price: number } | null>(null)
  const [paymentMethod, setPaymentMethod] = useState<'paystack-card' | 'paystack-alt' | 'snapscan'>('paystack-card')

  const subtotal = ORDER_TOTAL
  const deliveryFee = delivery?.price || 0
  const total = subtotal + deliveryFee

  return (
    <div className="min-h-screen">
      <Navbar />
      {showAuthModal && <SocialAuthModal onClose={closeAuth} />}

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-24">
        <h1 className="font-serif text-3xl text-bark-800 mb-12">Checkout</h1>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Left: delivery + auth */}
          <div className="space-y-8">
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

            <BobGoDelivery orderValueZAR={ORDER_TOTAL} onSelect={setDelivery} />
          </div>

          {/* Right: order summary */}
          <div>
            <div className="bg-cream-50 rounded-2xl border border-cream-200 p-6 space-y-4">
              <h3 className="font-serif text-lg text-bark-800">Order summary</h3>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-bark-700/80">Subtotal</span>
                  <span className="font-mono">R {subtotal}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-bark-700/80">Delivery</span>
                  <span className="font-mono">{deliveryFee > 0 ? `R ${deliveryFee}` : '—'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-bark-700/80">VAT (15%)</span>
                  <span className="font-mono">R {Math.round(total * TAX_RATE / (1 + TAX_RATE))}</span>
                </div>
              </div>

              <div className="border-t border-cream-300 pt-4 flex justify-between font-medium">
                <span className="font-serif text-bark-800">Total</span>
                <span className="font-mono text-bark-800">R {total}</span>
              </div>

              <CharitableGiving orderTotalZAR={total} />

              <div className="space-y-3">
                <p className="text-xs font-medium uppercase tracking-[0.18em] text-bark-700/60">Payment method</p>
                <label className="flex gap-3 rounded-xl border border-cream-300 bg-white/50 p-3 text-sm">
                  <input
                    type="radio"
                    name="payment-method"
                    value="paystack-card"
                    checked={paymentMethod === 'paystack-card'}
                    onChange={() => setPaymentMethod('paystack-card')}
                  />
                  <span>
                    <span className="block font-medium text-bark-800">Card with Paystack</span>
                    <span className="block text-xs text-bark-700/60">Working card checkout. Keep this as the fastest option.</span>
                  </span>
                </label>
                <label className="flex gap-3 rounded-xl border border-cream-300 bg-white/50 p-3 text-sm">
                  <input
                    type="radio"
                    name="payment-method"
                    value="paystack-alt"
                    checked={paymentMethod === 'paystack-alt'}
                    onChange={() => setPaymentMethod('paystack-alt')}
                  />
                  <span>
                    <span className="block font-medium text-bark-800">Paystack alternatives</span>
                    <span className="block text-xs text-bark-700/60">Shows any wallet, EFT, bank transfer, or CapitecPay options enabled on Paystack.</span>
                  </span>
                </label>
                <label className="flex gap-3 rounded-xl border border-cream-300 bg-white/50 p-3 text-sm">
                  <input
                    type="radio"
                    name="payment-method"
                    value="snapscan"
                    checked={paymentMethod === 'snapscan'}
                    onChange={() => setPaymentMethod('snapscan')}
                  />
                  <span>
                    <span className="block font-medium text-bark-800">SnapScan QR</span>
                    <span className="block text-xs text-bark-700/60">Setup required: add the Banimal SnapScan merchant QR or payment link before taking live payments.</span>
                  </span>
                </label>
              </div>

              {paymentMethod === 'snapscan' && (
                <p className="rounded-xl border border-amber-200 bg-amber-50 p-3 text-xs leading-relaxed text-amber-900">
                  SnapScan is selected, but no live SnapScan merchant payment link is configured yet. Use Paystack for this order, then add the SnapScan merchant QR/link to activate this option.
                </p>
              )}

              <a
                href={`https://banimal.co.za/checkout?source=faa&total=${total}&delivery=${delivery?.service || ''}&payment=${paymentMethod}`}
                aria-disabled={paymentMethod === 'snapscan'}
                className={`btn-primary w-full justify-center rounded-xl mt-2 text-sm ${paymentMethod === 'snapscan' ? 'pointer-events-none opacity-50' : ''}`}
              >
                {paymentMethod === 'paystack-alt' ? 'Continue to Paystack options' : paymentMethod === 'snapscan' ? 'SnapScan setup required' : 'Pay with Paystack card'}
              </a>

              <p className="text-xs text-center text-bark-700/40 mt-2">
                {paymentMethod === 'paystack-alt'
                  ? 'Paystack will show the available non-card options enabled on the merchant account.'
                  : paymentMethod === 'snapscan'
                    ? 'SnapScan needs a live merchant QR/link before checkout can process this payment.'
                    : 'Secure checkout powered by Paystack · Card checkout is live'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
