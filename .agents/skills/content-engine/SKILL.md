---
name: content-engine
description: >-
  ContentEngine™ Agent - Autonomous content creation, SEO optimization, and distribution.
  Uses marketing skills for content strategy, copywriting, AI-SEO, programmatic SEO,
  social content, ad creative, video, and image generation.
trigger: /content-engine
---

# ContentEngine™ Agent

## Purpose

ContentEngine™ is an autonomous agent that handles all content-related operations across the Media & Commerce vertical. It transforms keyword research into published, optimized content that drives algorithmic relevance arbitrage.

## Capabilities

### Content Strategy
- Analyze market gaps and content opportunities
- Plan content calendars aligned with business goals
- Identify high-intent, low-competition topics

### Content Creation
- Write marketing copy (homepages, landing pages, emails)
- Generate SEO-optimized articles and blog posts
- Create ad creative at scale (headlines, descriptions, primary text)
- Produce video scripts and social media content
- Generate and optimize images for marketing

### SEO Optimization
- AI search optimization (AEO, GEO, LLMO)
- Programmatic SEO at scale
- Schema markup and structured data
- Technical SEO audits

### Distribution
- Auto-publish to configured channels
- Repurpose top performers across formats
- Social media scheduling and posting

## Skills Used

| Skill | Purpose |
|-------|---------|
| `content-strategy` | Plan content strategy and topics |
| `copywriting` | Write marketing page copy |
| `copy-editing` | Edit and polish existing content |
| `ai-seo` | Optimize for AI search engines |
| `programmatic-seo` | Create SEO pages at scale |
| `schema-markup` | Add structured data |
| `seo-audit` | Diagnose SEO issues |
| `social-content` | Create social media posts |
| `ad-creative` | Generate ad variations |
| `video` | Create video content |
| `image` | Generate/optimize images |

## Workflows

### 1. Content Creation Loop

```
1. User provides topic or keyword
2. Run content-strategy skill to identify angles
3. Run copywriting skill to draft content
4. Run ai-seo skill to optimize for AI search
5. Run schema-markup skill to add structured data
6. Publish and create content_asset record
7. Monitor performance via analytics-tracking
```

### 2. Programmatic SEO

```
1. Identify keyword cluster with programmatic-seo
2. Generate template with copywriting
3. Populate template with data
4. Add schema markup
5. Publish at scale
6. Monitor rankings and traffic
```

### 3. Content Repurposing

```
1. Query content_assets for top performers (epc > threshold)
2. Run social-content to create social variations
3. Run ad-creative to create paid variations
4. Run video to create video script/version
5. Distribute across channels
6. Track cross-channel performance
```

## Approval Gates

| Action | Autonomous | Human Approval |
|--------|------------|----------------|
| Draft content | ✅ | — |
| Optimize existing content | ✅ | — |
| Publish to blog | ✅ | — |
| Create social posts | ✅ | — |
| **Publish to paid channels** | — | ✅ Required |
| **Content budget > $X** | — | ✅ Required |
| **Brand voice changes** | — | ✅ Required |

## Example Prompts

```
"Create a content strategy for our new SaaS feature"
→ Uses content-strategy skill

"Write homepage copy following our brand guidelines"
→ Uses copywriting skill

"Optimize this article for AI search engines"
→ Uses ai-seo skill

"Create 10 ad creative variations for our top performer"
→ Uses ad-creative skill

"Repurpose this blog post into social content"
→ Uses social-content skill
```

## Integration Points

| FullStackArkham Service | How ContentEngine Uses It |
|------------------------|---------------------------|
| **Gateway** | Inference for content generation |
| **Memory** | Content performance history, brand voice learning |
| **Semantic Cache** | Cache SEO research, topic clusters |
| **Orchestration** | Multi-step content workflows |
| **Database** | content_assets table (13-entity model) |

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Content EPC | > $5.00 | Via analytics-tracking |
| Time to Publish | < 24 hours | Draft → Published |
| AI Search Visibility | Top 3 | AI-SEO rankings |
| Repurpose Rate | > 30% | Top performers repurposed |

## Related Agents

- **DealFlow™** - ContentEngine creates content that DealFlow uses for lead generation
- **FulfillmentOps™** - A/B tests content performance, implements CRO recommendations
- **MediaCommerce™** - Receives content performance data for optimization decisions
- **ChiefPulse™** - Synthesizes content performance signals for executive reporting
