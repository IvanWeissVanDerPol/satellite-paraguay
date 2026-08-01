# Data Sheet — Verra VCS

**Dataset:** Verra Verified Carbon Standard (VCS) Registry
**Provider:** Verra
**License:** Public
**URL:** https://verra.org/

## Motivation

Verra VCS is the world's largest voluntary carbon market. Critical for P0100 Yvyra (carbon credit verification).

## Composition

- **Number of projects:** 2,000+ globally, 5+ in Paraguay
- **Project types:** REDD+, IFM, ARR, ALM
- **Methodologies:** 100+ (VM0007 REDD+ MF, AR-ACM0003, etc.)
- **Credits issued:** 1B+ tCO2e cumulative
- **Geographic coverage:** Global

## Collection process

- Projects registered with Verra
- Validated by accredited third-party auditors
- Monitored annually
- Verified via satellite + ground data

## Uses

- Source of carbon credit projects to verify (P0100 Yvyra)
- Cross-reference with Paraguayan INFONA registry
- Compute biomass + compare to claims

## Distribution

- **Registry:** https://registry.verra.org/
- **Search:** HTML form (no JSON API)
- **Format:** HTML
- **Real impl:** Scrape + parse

## Maintenance

- Updated by Verra as projects register/issue credits

## Limitations

- No clean JSON API
- Scraping requires careful rate limiting
- Project data may be outdated
- Paraguayan coverage is sparse (5 projects)

## Ethical considerations

- Public registry — no consent required
- Used for: climate policy, carbon markets, research
- Critical view: Verra has been criticized for low-quality credits
