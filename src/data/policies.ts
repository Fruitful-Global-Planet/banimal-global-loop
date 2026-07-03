import { RotateCcw, Truck, ShieldCheck, FileText, type LucideIcon } from 'lucide-react'

export const COMPANY = {
  company: 'Fruitful Shops (Pty) Ltd',
  tradingAs: 'Fruitful Banimal',
  reg: '2021/121654/07',
  vat: '4400302974',
  email: 'hello@banimal.co.za',
  refundEmail: 'kindrefund@banimal.co.za',
  location: 'Pretoria, Gauteng, South Africa',
} as const

export const POLICIES_LAST_UPDATED = '29 June 2026'

export type PolicyKind = 'returns' | 'shipping' | 'privacy' | 'terms'

export interface PolicySection {
  heading: string
  body: string[]
}

export interface Policy {
  icon: LucideIcon
  title: string
  path: string
  seoTitle: string
  seoDesc: string
  intro: string
  sections: PolicySection[]
}

export const POLICIES: Record<PolicyKind, Policy> = {
  returns: {
    icon: RotateCcw,
    title: 'Returns & Refund Policy',
    path: '/returns',
    seoTitle: 'Returns & Refund Policy | Banimal',
    seoDesc:
      'Fruitful Banimal returns and refund policy — how to return an item, refund timelines, and your rights under South African consumer law.',
    intro: `At ${COMPANY.tradingAs} we want you to love every order. If something is not right, we will make it right. This policy explains how returns, exchanges and refunds work, and applies to all purchases made on banimal.co.za.`,
    sections: [
      {
        heading: '1. Your right to return',
        body: [
          'You may return most items within 30 days of delivery for a refund or exchange, provided they are unworn, unwashed, in original condition and with any tags or packaging intact.',
          'Under the South African Consumer Protection Act, you may also cancel an order and return goods that are defective, not as described, or unsuitable for their intended purpose.',
        ],
      },
      {
        heading: '2. Items that cannot be returned',
        body: [
          'For hygiene reasons, items that have been worn, washed or soiled cannot be returned unless they are faulty.',
          'One-of-one original artworks and made-to-order handmade pieces are final sale unless they arrive damaged or defective.',
        ],
      },
      {
        heading: '3. How to start a return',
        body: [
          `Email ${COMPANY.refundEmail} with your order number, the item(s) you wish to return, and the reason. We reply within 1–2 business days with return instructions.`,
          'Do not ship anything back before you receive return instructions, so we can register your return and arrange collection or a return label where applicable.',
        ],
      },
      {
        heading: '4. Refunds',
        body: [
          'Once we receive and inspect your return, we will notify you of the outcome by email. Approved refunds are processed back to your original payment method.',
          'Refunds are typically completed within 5–10 business days of approval, depending on your bank or card issuer. The original delivery fee is refunded only where the return is due to our error or a defective item.',
          'Where a payment was made by card via Paystack, the refund is returned to the same card. We never request card details by email or phone.',
        ],
      },
      {
        heading: '5. Exchanges',
        body: [
          'If you need a different size, request an exchange when you start your return. Subject to stock, we will send the replacement once your original item is received and inspected.',
        ],
      },
      {
        heading: '6. Damaged or incorrect items',
        body: [
          `If your order arrives damaged, faulty, or incorrect, contact ${COMPANY.refundEmail} within 7 days of delivery with photos. We will arrange a free replacement or full refund, including delivery costs.`,
        ],
      },
      {
        heading: '7. Contact us',
        body: [
          `${COMPANY.company} (trading as ${COMPANY.tradingAs})`,
          `Returns & refunds: ${COMPANY.refundEmail}`,
          `General enquiries: ${COMPANY.email}`,
          `${COMPANY.location}`,
        ],
      },
    ],
  },
  shipping: {
    icon: Truck,
    title: 'Shipping & Delivery Policy',
    path: '/shipping',
    seoTitle: 'Shipping & Delivery Policy | Banimal',
    seoDesc:
      'Fruitful Banimal shipping and delivery policy — delivery times, courier partners, free shipping thresholds, and international delivery.',
    intro:
      'We ship across South Africa and worldwide. Orders are fulfilled through our courier partners and tracked door to door. This policy explains delivery times, costs and tracking.',
    sections: [
      {
        heading: '1. Order processing',
        body: [
          'Orders are processed within 1–2 business days after payment is confirmed. You receive an order confirmation email immediately, and a dispatch email with tracking once your parcel is collected.',
        ],
      },
      {
        heading: '2. Delivery times',
        body: [
          'South Africa: typically 2–5 business days depending on your location and the courier service selected at checkout.',
          'International: typically 5–14 business days depending on destination and customs clearance.',
        ],
      },
      {
        heading: '3. Shipping costs & free shipping',
        body: [
          'Live shipping rates are calculated at checkout based on your address and the courier you choose.',
          'Free shipping is automatically applied on local (South African) orders over R500, and on international orders over R1 500.',
        ],
      },
      {
        heading: '4. Tracking',
        body: [
          'Once dispatched, you will receive a tracking number by email. You will also receive out-for-delivery and delivered notifications as your parcel moves.',
        ],
      },
      {
        heading: '5. Customs & duties',
        body: [
          'International orders may be subject to import duties or taxes levied by the destination country. These are the responsibility of the recipient and are not included in the order total.',
        ],
      },
      {
        heading: '6. Contact us',
        body: [
          `${COMPANY.company} (trading as ${COMPANY.tradingAs})`,
          `Orders & delivery: ${COMPANY.email}`,
          `${COMPANY.location}`,
        ],
      },
    ],
  },
  privacy: {
    icon: ShieldCheck,
    title: 'Privacy Policy',
    path: '/privacy',
    seoTitle: 'Privacy Policy | Banimal',
    seoDesc:
      'Fruitful Banimal privacy policy — what personal information we collect, how we use it, and your rights under POPIA.',
    intro: `${COMPANY.company} respects your privacy. This policy explains what personal information we collect, why we collect it, and how we protect it, in line with South Africa's Protection of Personal Information Act (POPIA).`,
    sections: [
      {
        heading: '1. Information we collect',
        body: [
          'We collect the information you provide when you place an order or contact us: your name, email address, phone number, delivery address, and order details.',
          'Payment card details are processed securely by our payment provider (Paystack). We never see or store your full card number.',
        ],
      },
      {
        heading: '2. How we use your information',
        body: [
          'To process and deliver your orders, send order and delivery notifications, handle returns and refunds, respond to your enquiries, and — only if you opt in — send you news and special offers.',
        ],
      },
      {
        heading: '3. Sharing your information',
        body: [
          'We share information only as needed to fulfil your order: with our payment provider (Paystack) to process payment, and with our courier partners to deliver your parcel. We do not sell your personal information.',
        ],
      },
      {
        heading: '4. Your rights',
        body: [
          `You may request access to, correction of, or deletion of your personal information at any time by emailing ${COMPANY.email}. You may also unsubscribe from marketing emails at any time using the link in any email.`,
        ],
      },
      {
        heading: '5. Data security',
        body: [
          'We use industry-standard security measures and encrypted connections (HTTPS) to protect your information. Card payments are handled by PCI-DSS compliant providers.',
        ],
      },
      {
        heading: '6. Contact us',
        body: [
          `${COMPANY.company} (trading as ${COMPANY.tradingAs})`,
          `Privacy enquiries: ${COMPANY.email}`,
          `${COMPANY.location}`,
        ],
      },
    ],
  },
  terms: {
    icon: FileText,
    title: 'Terms & Conditions',
    path: '/terms',
    seoTitle: 'Terms & Conditions | Banimal',
    seoDesc: 'Fruitful Banimal terms and conditions of sale for purchases made on banimal.co.za.',
    intro: `These terms govern your use of banimal.co.za and any purchase you make from ${COMPANY.tradingAs}. By placing an order you agree to these terms.`,
    sections: [
      {
        heading: '1. About us',
        body: [
          `banimal.co.za is operated by ${COMPANY.company} (registration number ${COMPANY.reg}, VAT ${COMPANY.vat}), trading as ${COMPANY.tradingAs}, based in ${COMPANY.location}.`,
        ],
      },
      {
        heading: '2. Products & pricing',
        body: [
          'All prices are shown in South African Rand (ZAR) and include VAT where applicable. We make every effort to display products and prices accurately. If an error is found, we will contact you before processing your order.',
        ],
      },
      {
        heading: '3. Orders & payment',
        body: [
          'Your order is an offer to buy. A contract is formed once we confirm and accept your order. Payment is processed securely through Paystack at the time of checkout.',
        ],
      },
      {
        heading: '4. Returns & refunds',
        body: ['Returns and refunds are governed by our Returns & Refund Policy, which forms part of these terms.'],
      },
      {
        heading: '5. Limitation of liability',
        body: [
          'To the extent permitted by law, our liability for any claim relating to a product is limited to the price paid for that product. Nothing in these terms limits your rights under the Consumer Protection Act.',
        ],
      },
      {
        heading: '6. Governing law',
        body: ['These terms are governed by the laws of the Republic of South Africa.'],
      },
      {
        heading: '7. Contact us',
        body: [
          `${COMPANY.company} (trading as ${COMPANY.tradingAs})`,
          `Email: ${COMPANY.email}`,
          `${COMPANY.location}`,
        ],
      },
    ],
  },
}
