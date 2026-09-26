import { useState } from 'react'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import ProductCard, { type Product } from '@/components/ProductCard'
import CharitableGiving from '@/components/CharitableGiving'
import BasketBoost from '@/components/BasketBoost'
import { useAnalytics } from '@/contexts/AnalyticsContext'
import { useCart } from '@/contexts/CartContext'

const ALL_PRODUCTS: Product[] = [
  { id: 'BT001', name: 'Classic White Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT001-BYDvu1g2.png', category: 'Babygrow', sizes: ['0–3m'] },
  { id: 'BT002', name: 'Soft Grey Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT002-CX4CjBt9.png', category: 'Babygrow', sizes: ['0–3m'] },
  { id: 'BT003', name: 'Beige Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT003-Ynr1ODEe.png', category: 'Babygrow', sizes: ['3–6m'] },
  { id: 'BT004', name: 'Sage Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT004-KZ5X0Ak7.png', category: 'Babygrow', sizes: ['3–6m'] },
  { id: 'BT005', name: 'Blush Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT005-Ce7QfnBe.png', category: 'Babygrow', sizes: ['6–9m'] },
  { id: 'BT007', name: 'Storm Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT007-C5WxSB9Q.png', category: 'Babygrow', sizes: ['6–9m'] },
  { id: 'BT008', name: 'Caramel Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT008-Ci-PewEt.png', category: 'Babygrow', sizes: ['0–3m'] },
  { id: 'BT009', name: 'Slate Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT009-BYEat297.png', category: 'Babygrow', sizes: ['3–6m'] },
  { id: 'BT010', name: 'Ivory Babygrow', price: 289, image: 'https://banimal.co.za/assets/BT010-pzlVe3nP.png', category: 'Babygrow', sizes: ['6–9m'] },
  { id: 'BR001', name: 'Bandana Bib — Oatmeal', price: 129, image: 'https://banimal.co.za/assets/BR001-B9Svc9IF.png', category: 'Bib', isNew: true },
  { id: 'BR002', name: 'Bandana Bib — Slate', price: 129, image: 'https://banimal.co.za/assets/BR002-m4ScX5Ak.png', category: 'Bib', isNew: true },
  { id: 'PR001', name: 'Magical Forest', price: 500, image: '/assets/prints/print-portrait-01.jpg', category: 'Print', isNew: true },
  { id: 'PR002', name: 'Happy Place', price: 500, image: '/assets/prints/print-portrait-02.jpg', category: 'Print', isNew: true },
  { id: 'PR003', name: 'Monster Prints', price: 500, image: '/assets/prints/print-portrait-03.jpg', category: 'Print', isNew: true },
  { id: 'PR004', name: 'Loved', price: 500, image: '/assets/prints/print-portrait-04.jpg', category: 'Print', isNew: true },
  { id: 'PR005', name: 'Animal Prints', price: 500, image: '/assets/prints/print-portrait-05.jpg', category: 'Print', isNew: true },
  { id: 'PR006', name: 'Magical Landscape', price: 500, image: '/assets/prints/print-portrait-06.jpg', category: 'Print', isNew: true },
  { id: 'PR007', name: 'Wildlings', price: 500, image: '/assets/prints/print-portrait-07.jpg', category: 'Print', isNew: true },
]

const CATS = ['All', 'Babygrow', 'Bib', 'Print']

export default function Shop() {
  const [cat, setCat] = useState('All')
  const { items, addItem, subtotal } = useCart()
  const [basketOpen, setBasketOpen] = useState(false)
  const [lastAdded, setLastAdded] = useState<Product | null>(null)
  const { getHotItems, getColdItems } = useAnalytics()

  const filtered = cat === 'All' ? ALL_PRODUCTS : ALL_PRODUCTS.filter((p) => p.category === cat)
  const hotIds = getHotItems()
  const coldIds = getColdItems(ALL_PRODUCTS.map((p) => p.id))

  const getBadge = (id: string): 'popular' | 'new' | 'unseen' | undefined => {
    if (hotIds.includes(id)) return 'popular'
    if (coldIds.includes(id)) return 'unseen'
    return undefined
  }

  const addToCart = (product: Product) => {
    addItem(product)
    setLastAdded(product)
    setBasketOpen(true)
  }

  return (
    <div className="min-h-screen">
      <Navbar />
      <BasketBoost open={basketOpen} items={items} catalog={ALL_PRODUCTS} lastAdded={lastAdded} onAdd={addToCart} onClose={() => setBasketOpen(false)} />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-24">
        <div className="mb-12">
          <p className="label-tag mb-2">Collection</p>
          <h1 className="font-serif text-4xl text-bark-800">Shop all</h1>
        </div>

        <div className="flex gap-3 mb-10 flex-wrap">
          {CATS.map((c) => (
            <button
              key={c}
              onClick={() => setCat(c)}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-colors ${
                cat === c
                  ? 'bg-bark-800 text-cream-100'
                  : 'bg-cream-200 text-bark-700 hover:bg-cream-300'
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6 mb-12">
          {filtered.map((p) => (
            <ProductCard key={p.id} product={p} onAdd={addToCart} badge={getBadge(p.id)} />
          ))}
        </div>

        {items.length > 0 && <CharitableGiving orderTotalZAR={subtotal} />}
      </div>

      <Footer />
    </div>
  )
}
