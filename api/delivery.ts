import { VercelRequest, VercelResponse } from '@vercel/node'

const BOBGO_API_KEY = process.env.BOBGO_API_KEY || ''
const BOBGO_API_URL = 'https://api.bobgodelivery.com/v1'

// Delivery rules
const SA_FREE_THRESHOLD = 500 // R500 for free delivery in South Africa
const INTL_FREE_THRESHOLD = 1500 // R1500 for free delivery internationally
const SA_STANDARD_RATE = 85 // R85 for paid delivery in SA
const SA_EXPRESS_RATE = 145 // R145 for express in SA
const INTL_STANDARD_RATE = 250 // R250 for paid delivery internationally
const INTL_EXPRESS_RATE = 450 // R450 for express internationally

// South African postal code ranges (simplified for common areas)
const SA_POSTAL_CODES = {
  JNB: /^[012][0-9]{3}$/, // Johannesburg: 0000-0299, 1000-1299, 2000-2299
  CPT: /^8[0-3][0-9]{2}$/, // Cape Town: 8000-8399
  DBN: /^4[0-1][0-9]{2}$/, // Durban: 4000-4199
  PTA: /^[01][2-3][0-9]{2}$/, // Pretoria: 0100-0399, 1200-1399
  BLM: /^[01][4-5][0-9]{2}$/, // Bloemfontein: 0500-0599, 1400-1499
}

function detectLocation(postalCode: string): 'SA' | 'INTL' {
  // South African postal codes are typically 4 digits (0000-9999)
  if (/^[0-9]{4}$/.test(postalCode)) {
    return 'SA'
  }
  return 'INTL'
}

async function getBobGoRates(
  postalCode: string,
  orderValueZAR: number,
  location: 'SA' | 'INTL'
) {
  try {
    // Call BobGo API to get real rates
    const response = await fetch(`${BOBGO_API_URL}/rates`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${BOBGO_API_KEY}`,
      },
      body: JSON.stringify({
        postalCode,
        weight: 1, // Typical Banimal item weight in kg
        destination: location === 'SA' ? 'ZA' : 'INTL',
      }),
    })

    if (response.ok) {
      const data = (await response.json()) as {
        rates?: Array<{ service: string; price: number; days: string }>
      }
      return data.rates || null
    }
  } catch (error) {
    console.error('[v0] BobGo API error:', error)
  }
  return null
}

function getDefaultRates(location: 'SA' | 'INTL'): Array<{ service: string; price: number; days: string }> {
  if (location === 'SA') {
    return [
      { service: 'Standard Delivery', price: SA_STANDARD_RATE, days: '2–3 business days' },
      { service: 'Express Delivery', price: SA_EXPRESS_RATE, days: 'Next business day' },
    ]
  }
  return [
    { service: 'Standard Delivery', price: INTL_STANDARD_RATE, days: '5–10 business days' },
    { service: 'Express Delivery', price: INTL_EXPRESS_RATE, days: '2–3 business days' },
  ]
}

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true')
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT')
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  )

  if (req.method === 'OPTIONS') {
    res.status(200).end()
    return
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { toPostalCode, orderValueZAR } = req.body as {
    toPostalCode?: string
    orderValueZAR?: number
  }

  if (!toPostalCode || typeof orderValueZAR !== 'number') {
    return res.status(400).json({ error: 'Missing toPostalCode or orderValueZAR' })
  }

  // Detect location
  const location = detectLocation(toPostalCode)

  // Determine free shipping eligibility
  const freeThreshold = location === 'SA' ? SA_FREE_THRESHOLD : INTL_FREE_THRESHOLD
  const isFreeShipping = orderValueZAR >= freeThreshold

  // Get rates from BobGo API or use defaults
  let rates = await getBobGoRates(toPostalCode, orderValueZAR, location)
  if (!rates) {
    rates = getDefaultRates(location)
  }

  // Apply free shipping if order qualifies
  if (isFreeShipping) {
    rates = rates.map((r) => {
      // Remove the FREE suffix if it was already added during fallback
      const cleanService = r.service.replace(/\s*\(FREE\)$/, '')
      return {
        ...r,
        price: 0,
        service: `${cleanService} (FREE)`,
      }
    })
  }

  res.status(200).json({ rates, isFreeShipping, freeThreshold })
}
