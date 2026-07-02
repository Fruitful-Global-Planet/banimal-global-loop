import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import type { Product } from '@/components/ProductCard'

interface CartCtx {
  items: Product[]
  addItem: (p: Product) => void
  removeItem: (index: number) => void
  clear: () => void
  subtotal: number
}

const Ctx = createContext<CartCtx | null>(null)

const STORE_KEY = 'bam_cart'

function load(): Product[] {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY) || '[]')
  } catch {
    return []
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<Product[]>(load)

  useEffect(() => {
    localStorage.setItem(STORE_KEY, JSON.stringify(items))
  }, [items])

  const addItem = (p: Product) => setItems((prev) => [...prev, p])
  const removeItem = (index: number) => setItems((prev) => prev.filter((_, i) => i !== index))
  const clear = () => setItems([])
  const subtotal = items.reduce((s, p) => s + p.price, 0)

  return (
    <Ctx.Provider value={{ items, addItem, removeItem, clear, subtotal }}>
      {children}
    </Ctx.Provider>
  )
}

export function useCart() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('useCart must be inside CartProvider')
  return ctx
}
