import { useEffect, useState } from 'react'
import { MapPin, Truck, Loader } from 'lucide-react'

interface Rate {
  service: string
  price: number
  days: string
}

interface Props {
  orderValueZAR: number
  onSelect: (rate: Rate) => void
}

// Same-origin by default. The previous hardcoded apex-domain URL
// (https://banimal.co.za/api/delivery) made this a cross-origin request from
// www.banimal.co.za, which the worker isn't routed for — the fetch would hang
// or fail instead of returning rates.
const API = (import.meta.env.VITE_DELIVERY_API_URL as string) || '/api/delivery'
const FETCH_TIMEOUT_MS = 8000
const FREE_DELIVERY_THRESHOLD_ZAR = 500

function fallbackRates(orderValueZAR: number): Rate[] {
  const free = orderValueZAR >= FREE_DELIVERY_THRESHOLD_ZAR
  return [
    { service: 'Standard Delivery', price: free ? 0 : 85, days: '3–5 business days' },
    { service: 'Express Delivery', price: free ? 60 : 145, days: '1–2 business days' },
  ]
}

export default function BobGoDelivery({ orderValueZAR, onSelect }: Props) {
  const [address, setAddress] = useState('')
  const [suburb, setSuburb] = useState('')
  const [city, setCity] = useState('')
  const [postalCode, setPostalCode] = useState('')
  const [rates, setRates] = useState<Rate[]>([])
  const [loading, setLoading] = useState(false)
  const [locating, setLocating] = useState(false)
  const [selected, setSelected] = useState<Rate | null>(null)

  const autofillLocation = () => {
    setLocating(true)
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const resp = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`
          )
          const data = await resp.json() as {
            address: {
              road?: string; suburb?: string; city?: string;
              town?: string; postcode?: string; house_number?: string
            }
          }
          const a = data.address
          setAddress(`${a.house_number || ''} ${a.road || ''}`.trim())
          setSuburb(a.suburb || '')
          setCity(a.city || a.town || '')
          setPostalCode(a.postcode || '')
        } catch {}
        setLocating(false)
      },
      () => setLocating(false)
    )
  }

  const getRates = async () => {
    if (!postalCode) return
    setLoading(true)
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS)
    try {
      const resp = await fetch(`${API}/rates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ toPostalCode: postalCode, orderValueZAR }),
        signal: controller.signal,
      })
      const data = await resp.json() as { rates: Rate[] }
      setRates(data.rates && data.rates.length > 0 ? data.rates : fallbackRates(orderValueZAR))
    } catch {
      setRates(fallbackRates(orderValueZAR))
    } finally {
      clearTimeout(timeout)
      setLoading(false)
    }
  }

  useEffect(() => {
    if (postalCode.length === 4) getRates()
  }, [postalCode])

  const pick = (r: Rate) => {
    setSelected(r)
    onSelect(r)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-serif text-lg text-bark-800">Delivery</h3>
        <button
          onClick={autofillLocation}
          disabled={locating}
          className="flex items-center gap-1 text-xs text-bark-700/60 hover:text-bark-800 transition-colors"
        >
          {locating ? <Loader className="w-3 h-3 animate-spin" /> : <MapPin className="w-3 h-3" />}
          Use my location
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <input
          className="col-span-2 w-full border border-cream-300 rounded-xl px-3 py-2.5 text-sm bg-cream-50 focus:outline-none focus:border-bark-700"
          placeholder="Street address"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
        <input
          className="border border-cream-300 rounded-xl px-3 py-2.5 text-sm bg-cream-50 focus:outline-none focus:border-bark-700"
          placeholder="Suburb"
          value={suburb}
          onChange={(e) => setSuburb(e.target.value)}
        />
        <input
          className="border border-cream-300 rounded-xl px-3 py-2.5 text-sm bg-cream-50 focus:outline-none focus:border-bark-700"
          placeholder="City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <input
          className="border border-cream-300 rounded-xl px-3 py-2.5 text-sm bg-cream-50 focus:outline-none focus:border-bark-700"
          placeholder="Postal code"
          value={postalCode}
          onChange={(e) => setPostalCode(e.target.value)}
          maxLength={4}
        />
      </div>

      {loading && (
        <div className="flex items-center gap-2 text-sm text-bark-700/60">
          <Loader className="w-4 h-4 animate-spin" />
          Getting rates…
        </div>
      )}

      {rates.length > 0 && (
        <div className="space-y-2">
          {rates.map((r) => (
            <button
              key={r.service}
              onClick={() => pick(r)}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-xl border text-sm transition-colors ${
                selected?.service === r.service
                  ? 'border-bark-800 bg-bark-800/5'
                  : 'border-cream-300 hover:border-bark-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <Truck className="w-4 h-4 text-bark-700/60" />
                <div className="text-left">
                  <p className="font-medium text-bark-800">{r.service}</p>
                  <p className="text-xs text-bark-700/60">{r.days}</p>
                </div>
              </div>
              <span className="font-mono text-bark-800">R {r.price}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
