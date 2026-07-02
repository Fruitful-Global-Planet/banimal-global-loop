import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from '@/pages/Home'
import Shop from '@/pages/Shop'
import Checkout from '@/pages/Checkout'
import About from '@/pages/About'
import { AnalyticsProvider } from '@/contexts/AnalyticsContext'
import { AuthProvider } from '@/contexts/AuthContext'
import { ThemeProvider } from '@/contexts/ThemeContext'
import { CartProvider } from '@/contexts/CartContext'
import HoverCoupon from '@/components/HoverCoupon'
import PushNotificationBanner from '@/components/PushNotificationBanner'

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <CartProvider>
          <AnalyticsProvider>
            <Router>
              <PushNotificationBanner />
              <HoverCoupon />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/shop" element={<Shop />} />
                <Route path="/checkout" element={<Checkout />} />
                <Route path="/about" element={<About />} />
              </Routes>
            </Router>
          </AnalyticsProvider>
        </CartProvider>
      </AuthProvider>
    </ThemeProvider>
  )
}
