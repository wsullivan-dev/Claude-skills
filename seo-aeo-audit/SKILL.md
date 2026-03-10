---
name: seo-aeo-audit
description: Audit any webpage for SEO and AEO (Answer Engine Optimization) readiness. Checks meta tags, structured data (JSON-LD), heading hierarchy, content quality, internal linking, mobile readiness, and AI-discoverability signals. Use when users want to check SEO health, validate schema markup, or prepare content for AI search engines.
---

# SEO / AEO Audit

Audit a webpage for search engine optimization (SEO) and answer engine optimization (AEO) readiness.

## When to Use This Skill

Use this skill when users request:
- "Audit this page for SEO"
- "Check the SEO on my website"
- "Is this page AEO ready?"
- "Validate the JSON-LD on this page"
- "Check structured data"
- "How will AI search engines see this page?"
- Any request involving SEO analysis, schema validation, or AEO readiness

## Workflow

### Step 1: Fetch the Page

Use WebFetch to retrieve the target URL's HTML content. If auditing a local build file, read it directly.

```
Target URL provided by user, or default to https://getpacerai.com
```

### Step 2: Run the Audit

Analyze the HTML for the following categories, scoring each 0-100:

#### A. Technical SEO (weight: 25%)
- [ ] Title tag present, 50-60 chars, includes primary keyword
- [ ] Meta description present, 150-160 chars, compelling
- [ ] Canonical URL set
- [ ] Open Graph tags (og:title, og:description, og:image, og:url)
- [ ] Twitter Card tags
- [ ] Viewport meta tag for mobile
- [ ] Language attribute on `<html>`
- [ ] No duplicate H1 tags
- [ ] Clean URL structure (no query params, lowercase, hyphens)
- [ ] Internal links use descriptive anchor text

#### B. Content Quality (weight: 25%)
- [ ] Single H1 tag with primary keyword
- [ ] Logical heading hierarchy (H1 → H2 → H3, no skips)
- [ ] Sufficient content length (>300 words for pages, >800 for articles)
- [ ] Images have alt text
- [ ] No broken internal links
- [ ] Content matches search intent (informational, transactional, navigational)
- [ ] Unique value proposition clearly stated above the fold

#### C. Structured Data / Schema (weight: 25%)
- [ ] JSON-LD present and valid
- [ ] Appropriate @type for page context (Article, Organization, WebPage, FAQPage, etc.)
- [ ] Required properties populated (headline, author, datePublished for articles)
- [ ] Publisher with logo
- [ ] No schema errors (missing required fields, wrong types)
- [ ] Breadcrumb schema if applicable
- [ ] FAQ schema if page has Q&A content

#### D. AEO Readiness (weight: 25%)
- [ ] Clear, concise answers to likely questions (featured snippet format)
- [ ] Definition-style content ("What is X" → direct answer in first paragraph)
- [ ] Lists and tables for structured information
- [ ] FAQ section with clear Q&A pairs
- [ ] Entity relationships clear (who, what, for whom)
- [ ] Content structured for extraction (short paragraphs, clear sections)
- [ ] Expertise/authority signals (author info, citations, specific data points)

### Step 3: Generate Report

Output a formatted report with:

```markdown
# SEO/AEO Audit: [Page Title]
**URL:** [url]
**Date:** [today]
**Overall Score:** [X/100]

## Score Breakdown
| Category | Score | Grade |
|----------|-------|-------|
| Technical SEO | X/100 | A/B/C/D/F |
| Content Quality | X/100 | A/B/C/D/F |
| Structured Data | X/100 | A/B/C/D/F |
| AEO Readiness | X/100 | A/B/C/D/F |

## Findings

### ✅ Passing
- [items that pass]

### ⚠️ Warnings
- [items that could be improved]

### ❌ Failing
- [items that need immediate attention]

## Priority Fixes
1. [highest impact fix]
2. [second highest]
3. [third highest]

## Structured Data Validation
[JSON-LD found: yes/no]
[Schema types detected]
[Validation result]
```

### Step 4: Save Report

Save the audit report to the project's review directory:
```
docs/review/seo-audit-[domain]-[YYYYMMDD].md
```

## Grading Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent — production ready |
| 80-89 | B | Good — minor improvements recommended |
| 70-79 | C | Fair — several issues to address |
| 60-69 | D | Poor — significant gaps |
| 0-59 | F | Failing — major rework needed |

## AEO-Specific Guidance

Answer Engine Optimization focuses on making content discoverable by AI systems (ChatGPT, Perplexity, Google AI Overviews, Copilot). Key differences from traditional SEO:

1. **Direct answers** — AI engines extract concise answers. Structure content as Q&A.
2. **Entity clarity** — Clearly define what your product/service IS in the first 2 sentences.
3. **Structured data** — JSON-LD is the primary way AI systems understand page relationships.
4. **Specificity** — Concrete numbers, comparisons, and examples are preferred over vague claims.
5. **Topical authority** — Multiple related pages with internal links signal expertise.
