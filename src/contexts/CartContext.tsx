import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import type { Product } from '@/components/ProductCard'

export interface CartItem extends Product {
  quantity: number
  /** For art licences: the selected licence tier */
  licenceTier?: string
  /** For art licences: the artwork title */
  artworkTitle?: string
}

interface CartContextValue {
  items: CartItem[]
  count: number
  total: number
  addItem: (product: Product, quantity?: number, licenceTier?: string, artworkTitle?: string) => void
  removeItem: (id: string, licenceTier?: string) => void
  updateQuantity: (id: string, quantity: number, licenceTier?: string) => void
  clearCart: () => void
}

const CartContext = createContext<CartContextValue | null>(null)

const STORAGE_KEY = 'banimal_cart_v1'

function loadCart(): CartItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    return JSON.parse(raw) as CartItem[]
  } catch {
    return []
  }
}

function saveCart(items: CartItem[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
  } catch {
    // ignore storage errors (private browsing, quota exceeded)
  }
}

/** Unique key per cart line: product id + optional licence tier */
function lineKey(id: string, licenceTier?: string) {
  return licenceTier ? `${id}::${licenceTier}` : id
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>(loadCart)

  useEffect(() => {
    saveCart(items)
  }, [items])

  const count = items.reduce((s, i) => s + i.quantity, 0)
  const total = items.reduce((s, i) => s + i.price * i.quantity, 0)

  function addItem(product: Product, quantity = 1, licenceTier?: string, artworkTitle?: string) {
    const key = lineKey(product.id, licenceTier)
    setItems((prev) => {
      const existing = prev.find((i) => lineKey(i.id, i.licenceTier) === key)
      if (existing) {
        return prev.map((i) =>
          lineKey(i.id, i.licenceTier) === key
            ? { ...i, quantity: i.quantity + quantity }
            : i
        )
      }
      return [...prev, { ...product, quantity, licenceTier, artworkTitle }]
    })
  }

  function removeItem(id: string, licenceTier?: string) {
    const key = lineKey(id, licenceTier)
    setItems((prev) => prev.filter((i) => lineKey(i.id, i.licenceTier) !== key))
  }

  function updateQuantity(id: string, quantity: number, licenceTier?: string) {
    const key = lineKey(id, licenceTier)
    if (quantity <= 0) {
      removeItem(id, licenceTier)
      return
    }
    setItems((prev) =>
      prev.map((i) => (lineKey(i.id, i.licenceTier) === key ? { ...i, quantity } : i))
    )
  }

  function clearCart() {
    setItems([])
  }

  return (
    <CartContext.Provider value={{ items, count, total, addItem, removeItem, updateQuantity, clearCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used inside CartProvider')
  return ctx
}
