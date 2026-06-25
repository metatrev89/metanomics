# Metanomics SEO/AEO Plan
*Generated June 24, 2026*

---

## Part 1 — Technical GEO Audit

### ✅ Already in Good Shape

- **JSON-LD schema on homepage** — WebSite, Person, and all 3 Book formats (Paperback, Hardcover, Kindle) are implemented and correct
- **Open Graph + Twitter Card tags** — properly set on index.html
- **Canonical tag** — present on homepage
- **robots.txt** — clean, correct, includes sitemap reference
- **sitemap.xml** — exists and references the sitemap in robots.txt
- **H1 tag** — "METANOMICS" is the H1 on homepage
- **Google Analytics** — wired up (G-72229G51TF)
- **Image alt text** — present on key images
- **Mobile viewport** — set correctly

---

### ❌ Gaps to Fix

**Priority 1 — Blog post schema (critical for AI citation)**

Every blog post needs an `Article` JSON-LD block. Right now `posts/metanomics-overview-summaries.html` has zero schema. AI systems like ChatGPT and Perplexity heavily weight structured Article data when deciding what to cite.

Each post needs:
```json
{
  "@type": "Article",
  "headline": "...",
  "author": { "@id": "https://www.metanomics.org/#person" },
  "datePublished": "...",
  "dateModified": "...",
  "publisher": { "@id": "https://www.metanomics.org/#website" },
  "mainEntityOfPage": "https://www.metanomics.org/posts/slug.html",
  "image": "..."
}
```

**Priority 1 — BreadcrumbList schema on posts**

Adds navigational context for Google and AI:
```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.metanomics.org/" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.metanomics.org/blog.html" },
    { "@type": "ListItem", "position": 3, "name": "Post Title" }
  ]
}
```

**Priority 1 — FAQPage schema on blog posts**

For every post that includes a FAQ section, add `FAQPage` schema. This is one of the most reliable ways to get cited by AI assistants. A post like "Who is Metatron?" with 5 FAQ items becomes directly citeable.

**Priority 2 — VideoObject schema on homepage**

The YouTube video (VjbcU7p2jT8) should have schema:
```json
{
  "@type": "VideoObject",
  "name": "Metanomics: Reverse Engineering the Economy of Zion",
  "embedUrl": "https://www.youtube.com/embed/VjbcU7p2jT8",
  "thumbnailUrl": "https://i.ytimg.com/vi/VjbcU7p2jT8/maxresdefault.jpg",
  "uploadDate": "...",
  "publisher": { "@id": "https://www.metanomics.org/#person" }
}
```

**Priority 2 — Canonical tags missing on blog posts**

`posts/metanomics-overview-summaries.html` has no canonical tag. Add to all posts:
```html
<link rel="canonical" href="https://www.metanomics.org/posts/[slug].html">
```

**Priority 2 — Open Graph article metadata on posts**

Posts have `og:type = "article"` but are missing the companion tags:
```html
<meta property="article:published_time" content="2025-04-08T00:00:00Z">
<meta property="article:author" content="https://www.metanomics.org/#person">
<meta property="article:section" content="Prophecy">
```

**Priority 2 — Sitemap not auto-updated**

The sitemap only has 3 URLs and will go stale fast. The `sync_notion.py` script needs to regenerate `sitemap.xml` every time it publishes new posts. (Fix: add sitemap regeneration to the sync script.)

**Priority 3 — Ebook cover still on Wix CDN**

`https://static.wixstatic.com/media/2d97c8_...` loads from Wix. Move this image to `assets/images/` to remove the external dependency.

**Priority 3 — RSS feed**

Add an RSS feed (`/feed.xml`) so content aggregators and AI crawlers can discover new posts automatically.

---

## Part 2 — Keyword Research

### High-Traffic Entry Points

| Keyword | Why it matters |
|---|---|
| `who is Metatron` | Heavily searched. Christianity.com, GotQuestions, Wikipedia dominate — but they give surface-level answers. Trevor's angle (Metatron as Enoch + prophetic role in last days) is a real gap. |
| `Metatron Bible` | Related cluster — same opportunity |
| `Second Coming of Christ timeline` | Very active in 2026 — people are literally betting on it. High urgency content. |
| `return of Jesus signs` | Evergreen high-volume prophetic topic |
| `New Jerusalem Bible` | Strong search volume, mostly theological — economic angle is wide open |
| `all things in common Acts` / `all things in common meaning` | Regularly searched; most results are basic commentary, not economic analysis |
| `Metatron's Cube meaning` | Popular sacred geometry search; connects to the brand visually |
| `who was Enoch in the Bible` | Gateway to Metatron content |

### Mid-Tail Niche Keywords (Lower Competition)

| Keyword | Why it matters |
|---|---|
| `Economy of Zion` | Virtually no dedicated content outside LDS academic papers — Trevor owns this |
| `United Order economics` | LDS-specific, moderate volume, underserved |
| `law of consecration explained` | Good search volume in LDS community |
| `New Jerusalem economics` | Near-zero competition |
| `biblical economics` | Emerging topic, growing interest |
| `Zion society scripture` | Low competition, core to book thesis |
| `sacred economics Bible` | Almost no direct content |
| `prophecy and economics` | Unique angle, low competition |

### Long-Tail AI-Citation Targets

These are the kinds of questions AI assistants get asked that Trevor should rank for:

- "What does the Bible say about the Economy of Zion?"
- "How does Metatron relate to the Second Coming?"
- "What is all things in common in the New Testament?"
- "Who is Enoch and why does he matter in prophecy?"
- "What will the New Jerusalem look like economically?"
- "What is the United Order and how does it relate to Zion?"

---

## Part 3 — 30-Day Content Plan

**Cadence:** 3–4 posts per week. Aim for 1,500–2,500 words each. Every post gets Article + BreadcrumbList + FAQPage schema.

### Week 1 — Establish Core SEO Pillars (June 25 – July 1)

| # | Title | Target Keyword | Format |
|---|---|---|---|
| 1 | **Who Is Metatron? The Complete Scriptural Answer** | `who is Metatron`, `Metatron Bible` | Deep explainer + FAQ (5 Q&As) |
| 2 | **The Return of Jesus Timeline: What Scripture Actually Says** | `return of Jesus timeline`, `Second Coming timeline` | Structured timeline + FAQ |
| 3 | **What Does "All Things in Common" Mean? The Economics of the Early Church** | `all things in common meaning`, `all things in common Acts` | Explainer + modern application |

### Week 2 — Own the Niche (July 2 – July 8)

| # | Title | Target Keyword | Format |
|---|---|---|---|
| 4 | **What Is the Economy of Zion?** | `Economy of Zion`, `Zion economics` | Definitional pillar post |
| 5 | **The New Jerusalem Is an Economic System, Not Just a City** | `New Jerusalem Bible`, `New Jerusalem economics` | Argument/thesis post |
| 6 | **Metatron's Cube: Sacred Geometry and Its Biblical Meaning** | `Metatron's Cube meaning`, `sacred geometry Bible` | Visual explainer + FAQ |
| 7 | **The United Order vs. Modern Communism: What Scripture Actually Teaches** | `United Order economics`, `law of consecration` | Comparison post |

### Week 3 — Prophetic/Timely Angles (July 9 – July 15)

| # | Title | Target Keyword | Format |
|---|---|---|---|
| 8 | **2026 and Biblical Prophecy: Reading the Timeline Honestly** | `Second Coming 2026`, `prophecy 2026` | Timely/current events |
| 9 | **Signs of the Last Days: An Economic Perspective** | `signs of the last days`, `end times economics` | List post + FAQ |
| 10 | **Who Was Enoch? From Prophet to Heavenly Scribe** | `who was Enoch Bible`, `Enoch angel` | Biographical deep-dive |
| 11 | **The Law of Consecration: What It Is and Why It Still Matters** | `law of consecration explained`, `consecration LDS` | Explainer |

### Week 4 — Book-Specific / Author Authority (July 16 – July 22)

| # | Title | Target Keyword | Format |
|---|---|---|---|
| 12 | **Why Prophecy and Economics Are Inseparable** | `biblical economics`, `prophecy economics` | Thesis/manifesto |
| 13 | **Reverse Engineering Zion: How Scripture Describes a New Society** | `Zion society scripture`, `building Zion` | Long-form overview |
| 14 | **Metatron's Role in the Last Days: A Scriptural Case** | `Metatron last days`, `Metatron Second Coming` | Argument post + FAQ |
| 15 | **Sacred Economics: What Ancient Scripture Says About Money and Society** | `sacred economics`, `biblical economics system` | Big-picture synthesis |

---

## Part 4 — Next Actions

### Immediate (technical fixes, do first):
- [ ] Add Article + BreadcrumbList + FAQPage schema to `sync_notion.py` post template so every new post auto-gets schema
- [ ] Add canonical tag to post template
- [ ] Add OG article tags (`article:published_time`, `article:author`, `article:section`) to post template
- [ ] Add VideoObject schema to `index.html`
- [ ] Add sitemap auto-regeneration to `sync_notion.py`
- [ ] Move Wix CDN ebook cover to `assets/images/`

### Content (start publishing):
- [ ] Write and publish Post #1: "Who Is Metatron?"
- [ ] Set up scheduled weekly publishing via Notion MCP

### Indexing (after each publish):
- [ ] Run `python3 scripts/ping_bing.py` after every push
- [ ] Create `scripts/ping_google.py` (Google Search Console ping)
- [ ] Create `scripts/ping_all.py` (one command for all engines)
