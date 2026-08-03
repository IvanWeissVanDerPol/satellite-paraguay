# P0010 Yvyra — Carbon credit verification

- **Target:** Nature Climate Change (IF=28.9)
- **Status:** Draft complete, real Verra data integrated
- **Anchor:** First AI carbon credit verification for Paraguay
- **Scope:** 5 Verra projects, 123,000 ha, 2.5M tCO2e

## Run

```bash
cd /root/satellite-paraguay
python3 -c "
import sys
sys.path.insert(0, '.')
from src.external import fetch_verra_paraguay
verra = fetch_verra_paraguay()
print(verra.to_string())
"
```
