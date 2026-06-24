import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-bark-800 text-cream-200 mt-24">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Top grid — stacks to single column on mobile */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 mb-12">
          <div className="sm:col-span-2 md:col-span-1">
            <img src="https://banimal.co.za/assets/logo-white-Cn9gtfrc.png" alt="Banimal" className="h-8 mb-4" />
            <p className="text-cream-300 text-sm leading-relaxed">
              Premium 100% cotton baby essentials, thoughtfully designed in South Africa and shipped worldwide.
            </p>
            <p className="text-cream-400/70 text-xs mt-3">A Fruitful Global Planet brand</p>
          </div>
          <div>
            <p className="text-xs font-mono tracking-widest uppercase text-cream-400/80 mb-4">Shop</p>
            <ul className="space-y-2 text-sm text-cream-300">
              <li><Link to="/shop" className="hover:text-cream-100 transition-colors">Babygrows</Link></li>
              <li><Link to="/shop" className="hover:text-cream-100 transition-colors">Bibs</Link></li>
              <li><Link to="/shop" className="hover:text-cream-100 transition-colors">New Arrivals</Link></li>
            </ul>
          </div>
          <div>
            <p className="text-xs font-mono tracking-widest uppercase text-cream-400/80 mb-4">Company</p>
            <ul className="space-y-2 text-sm text-cream-300">
              <li><Link to="/about" className="hover:text-cream-100 transition-colors">About</Link></li>
              <li><a href="mailto:hello@banimal.co.za" className="hover:text-cream-100 transition-colors">Contact</a></li>
              <li><a href="https://fruitful.global" target="_blank" rel="noreferrer" className="hover:text-cream-100 transition-colors">Fruitful Global Planet</a></li>
            </ul>
          </div>
          <div>
            <p className="text-xs font-mono tracking-widest uppercase text-cream-400/80 mb-4">Connect</p>
            <ul className="space-y-2 text-sm text-cream-300">
              <li><a href="https://instagram.com/banimalza" target="_blank" rel="noreferrer" className="hover:text-cream-100 transition-colors">Instagram</a></li>
              <li><a href="https://facebook.com/banimalza" target="_blank" rel="noreferrer" className="hover:text-cream-100 transition-colors">Facebook</a></li>
              <li><a href="https://tiktok.com/@banimalza" target="_blank" rel="noreferrer" className="hover:text-cream-100 transition-colors">TikTok</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-bark-700 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
          <p className="text-cream-400 text-xs">&copy; {new Date().getFullYear()} Fruitful Global Planet (Pty) Ltd. All rights reserved.</p>
          <div className="flex items-center gap-2 text-xs text-cream-400">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse flex-shrink-0"></span>
            <span>15.01% of every sale supports children in need</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
