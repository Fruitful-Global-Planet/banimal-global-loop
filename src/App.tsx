import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from '@/pages/Home'
import Shop from '@/pages/Shop'
import Checkout from '@/pages/Checkout'
import About from '@/pages/About'
import Policy from '@/pages/Policy'
import { AnalyticsProvider } from '@/contexts/AnalyticsContext'
import { AuthProvider } from '@/contexts/AuthContext'
import HoverCoupon from '@/components/HoverCoupon'
import PushNotificationBanner from '@/components/PushNotificationBanner'

export default function App() {
  return (
    <AuthProvider>
      <AnalyticsProvider>
        <Router>
          <PushNotificationBanner />
          <HoverCoupon />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/shop" element={<Shop />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/about" element={<About />} />
            <Route path="/returns" element={<Policy kind="returns" />} />
            <Route path="/shipping" element={<Policy kind="shipping" />} />
            <Route path="/privacy" element={<Policy kind="privacy" />} />
            <Route path="/terms" element={<Policy kind="terms" />} />
          </Routes>
        </Router>
      </AnalyticsProvider>
    </AuthProvider>
  )
}
