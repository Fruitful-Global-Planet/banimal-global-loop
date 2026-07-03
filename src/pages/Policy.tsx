import { useEffect } from 'react'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import { POLICIES, POLICIES_LAST_UPDATED, type PolicyKind } from '@/data/policies'

export default function Policy({ kind }: { kind: PolicyKind }) {
  const policy = POLICIES[kind]
  const Icon = policy.icon

  useEffect(() => {
    document.title = policy.seoTitle
    const meta = document.querySelector('meta[name="description"]')
    if (meta) meta.setAttribute('content', policy.seoDesc)
    window.scrollTo(0, 0)
  }, [policy])

  return (
    <div className="min-h-screen">
      <Navbar />

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-24">
        <div className="flex items-center gap-3 mb-2">
          <span className="flex h-11 w-11 items-center justify-center rounded-full bg-bark-800 text-cream-100">
            <Icon className="h-5 w-5" />
          </span>
          <h1 className="font-serif text-3xl sm:text-4xl text-bark-800">{policy.title}</h1>
        </div>

        <p className="text-sm text-bark-700/60 mb-6">Last updated {POLICIES_LAST_UPDATED}</p>

        <p className="text-base leading-relaxed text-bark-700 mb-10">{policy.intro}</p>

        <div className="space-y-8">
          {policy.sections.map((section) => (
            <section key={section.heading}>
              <h2 className="font-serif text-xl text-bark-800 mb-3">{section.heading}</h2>
              <div className="space-y-3">
                {section.body.map((paragraph, i) => (
                  <p key={i} className="text-sm leading-relaxed text-bark-700">
                    {paragraph}
                  </p>
                ))}
              </div>
            </section>
          ))}
        </div>
      </div>

      <Footer />
    </div>
  )
}
