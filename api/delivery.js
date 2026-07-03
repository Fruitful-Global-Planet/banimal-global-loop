// BobGo Delivery Rates API
// Handles delivery rate calculations based on location and order value
// Free shipping: SA R500+, International R1500+

const BOBGO_API_KEY = process.env.BOBGO_API_KEY || ''
const BOBGO_API_URL = 'https://api.bobgodelivery.com/v1'

// Delivery thresholds and rates
const SA_FREE_THRESHOLD = 500
const INTL_FREE_THRESHOLD = 1500
const SA_STANDARD = 85
const SA_EXPRESS = 145
const INTL_STANDARD = 250
const INTL_EXPRESS = 450

/**
 * Detect if postal code is South African (4 digits) or international
 */
function isSouthAfrican(postalCode) {
  return /^\d{4}$/.test(postalCode)
}

/**
 * Get delivery rates based on location and order value
 */
function getDeliveryRates(toPostalCode, orderValueZAR) {
  const isInternational = !isSouthAfrican(toPostalCode)
  const freeThreshold = isInternational ? INTL_FREE_THRESHOLD : SA_FREE_THRESHOLD
  const qualifiesForFree = orderValueZAR >= freeThreshold

  let rates = []

  if (isInternational) {
    // International rates
    rates = [
      {
        service: 'Standard Delivery',
        days: '7-10 business days',
        price: qualifiesForFree ? 0 : INTL_STANDARD,
      },
      {
        service: 'Express Delivery',
        days: '3-5 business days',
        price: qualifiesForFree ? 0 : INTL_EXPRESS,
      },
    ]
  } else {
    // South African rates
    rates = [
      {
        service: 'Standard Delivery',
        days: '1-2 business days',
        price: qualifiesForFree ? 0 : SA_STANDARD,
      },
      {
        service: 'Express Delivery',
        days: 'Next business day',
        price: qualifiesForFree ? 0 : SA_EXPRESS,
      },
    ]
  }

  return {
    rates,
    location: isInternational ? 'International' : 'South Africa',
    freeThreshold,
    isFreeShipping: qualifiesForFree,
  }
}

/**
 * Vercel serverless function handler
 */
export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true')
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT')
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version')

  if (req.method === 'OPTIONS') {
    res.status(200).end()
    return
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { toPostalCode, orderValueZAR } = req.body

    if (!toPostalCode || orderValueZAR === undefined) {
      return res.status(400).json({
        error: 'Missing required fields: toPostalCode, orderValueZAR',
      })
    }

    const ratesData = getDeliveryRates(toPostalCode, orderValueZAR)

    res.status(200).json(ratesData)
  } catch (error) {
    console.error('Delivery API Error:', error)
    res.status(500).json({
      error: 'Failed to calculate delivery rates',
      message: error.message,
    })
  }
}
