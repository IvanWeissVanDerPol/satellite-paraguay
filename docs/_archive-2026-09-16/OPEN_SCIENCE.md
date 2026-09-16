# Open Science Plan

**Goal:** Maximize reproducibility, citation, and impact through open science practices.

## 1. Zenodo Deposit

### What to deposit

**Code repository (DOI):**
- satellite-paraguay codebase
- Version 1.0 (semantic versioning)
- License: MIT
- Files: All .py, .md, .yml (not large data)
- DOI issued via Zenodo-GitHub integration

**Dataset (DOI):**
- Derived datasets (Hansen subset, MapBiomas, Sentinel-2)
- 2.7 GB (fits Zenodo limits)
- License: CC-BY-SA 4.0
- Files: TIF, CSV, JSON

**Thesis (DOI):**
- Final thesis as PDF
- ~50,000 words
- License: CC-BY-SA 4.0

### How to deposit

```bash
# Install zenodo CLI
pip install zenodo-records

# Authenticate
zenodo auth

# Create deposit
zenodo create --title "satellite-paraguay v1.0" \\
              --description "Multi-temporal satellite computer vision for Paraguay" \\
              --license MIT \\
              --community satellite-paraguay

# Upload files
zenodo upload file.zip

# Publish
zenodo publish
```

### Schedule

- v0.5 deposit: 2026-09 (after IRB + Prithvi run)
- v1.0 deposit: 2027-02 (after thesis defense)

## 2. DOI Strategy

### What gets DOIs

- Code (every release): 1 DOI per version
- Dataset (annually): 1 DOI per year
- Thesis: 1 DOI for final version
- Preprints: 1 DOI per paper

### DOI providers

- Code: Zenodo (free, immediate)
- Data: Zenodo (free, 50 GB limit)
- Papers: arXiv (free) + DOI via Crossref

## 3. License Strategy

### Code: MIT License
```
MIT License

Copyright (c) 2026 Iván Hocht-VonDerPol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

### Data: CC-BY-SA 4.0
- Allows commercial reuse
- Requires attribution
- Requires share-alike

### Thesis: CC-BY-SA 4.0
- Open access
- Free to share and adapt

### Indigenous community data: Community-controlled
- NOT publicly shared without FPIC
- Documented in etica/FPIC_template_es.md

## 4. Reproducibility Badge

Apply for **Reproducibility Badge** from ACM or NeurIPS:
- Code publicly available ✓
- Data publicly available ✓
- Results independently verified (after reproducibility check) ✓

## 5. Preprint Strategy

### Preprint servers
- **arXiv** (cs.LG, cs.CV, stat.AP): Free, immediate, indexed
- **bioRxiv** (biology adjacent): For ecology work
- **EarthArXiv** (earth observation): For RS work
- **SSRN** (social science): For Yvy indigenous work

### Preprint timing
- P0011 Yvutu: Submit 2026-10 (after Prithvi run)
- P0010 Yvyra: Submit 2026-11
- P0012 Yvy: Submit 2026-12

## 6. Open Peer Review

- Publish reviewer reports alongside papers
- Respond openly to reviews
- Encourage open discussion

## 7. Citation

All papers, data, and code should cite the underlying data sources:

**Hansen:**
> Hansen, M. C., et al. (2013). "High-Resolution Global Maps of 21st-Century Forest Cover Change." *Science*.

**MapBiomas:**
> MapBiomas Paraguay. (2023). "MapBiomas Paraguay Collection 2."

**Sentinel-2:**
> ESA. (2015). "Sentinel-2 User Handbook."

**Prithvi:**
> NASA-IBM Hugging Face Team. (2023). "Prithvi-100M."

## 8. Community Engagement

### Mailing list
- Google Group: satellite-paraguay@googlegroups.com
- Quarterly newsletter

### Forum
- GitHub Discussions: github.com/IvanWeissVanDerPol/satellite-paraguay/discussions
- Categories: Help, Ideas, Show and tell

### Office hours
- Monthly Zoom office hours
- Posted on GitHub Discussions

### Workshops
- Annual workshop in Asunción
- Online tutorials on YouTube

## 9. Impact Tracking

### Citation count
- Google Scholar profile
- Track citation count quarterly

### Usage tracking
- GitHub stars, forks, clones
- PyPI downloads
- Zenodo download count

### Societal impact
- Policy briefs adopted
- Media coverage
- Stakeholder testimonials

## 10. Long-term Sustainability

### Funding
- Grants: NSF, ERC, IDB, World Bank
- Industry partnerships
- Consulting revenue

### Maintenance
- Bug fixes
- Dependency updates
- New data sources

### Succession
- Train 1-2 PhD students per year
- Document all processes
- Open governance model

---

## Implementation Timeline

| Date | Milestone |
|---|---|
| 2026-08 | Zenodo account created |
| 2026-09 | v0.5 deposit (after IRB + Prithvi) |
| 2026-10 | arXiv preprint of P0011 |
| 2026-11 | arXiv preprint of P0010 |
| 2026-12 | arXiv preprint of P0012 |
| 2027-02 | v1.0 deposit (thesis + all data) |
| 2027-03 | Workshop in Asunción |

---

**This document is updated quarterly by Erebus (autonomous agent).**