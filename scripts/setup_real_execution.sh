#!/usr/bin/env bash
# Real-data setup guide for SatelliteCV-Paraguay
#
# This script does NOT auto-run anything. It prints instructions and
# (optionally) opens URLs for the user to act on.
#
# Usage:
#   ./scripts/setup_real_execution.sh [--auto]   # interactive / non-interactive

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "============================================================"
echo "SatelliteCV-Paraguay — Real-Data Setup Guide"
echo "============================================================"
echo ""
echo "This setup unlocks REAL data and REAL training. The pilot experiment"
echo "in outputs/p0011/ uses synthetic data because the following accounts"
echo "and APIs are not yet configured."
echo ""

# 1. Google Earth Engine
echo "1. GOOGLE EARTH ENGINE (for Sentinel-2 + Hansen)"
echo "   - Sign up: https://signup.earthengine.google.com/ (free, 1 min)"
echo "   - Install: pip install earthengine-api"
echo "   - Authenticate: earthengine authenticate"
echo "   - Verify:   python3 -c 'import ee; ee.Initialize()'"
echo ""

# 2. OpenAQ (for P0035)
echo "2. OPENAQ v3 (for P0035 Tatakua air quality)"
echo "   - Sign up: https://openaq.org/ (free)"
echo "   - Get API key at https://openaq.org/account"
echo "   - Set env var: export OPENAQ_API_KEY='your_key_here'"
echo ""

# 3. NASA FIRMS (for P0026)
echo "3. NASA FIRMS (for P0026 Kai fire detection)"
echo "   - Sign up: https://firms.modaps.eosdis.nasa.gov/api/"
echo "   - Get MAP_KEY"
echo "   - Set env var: export FIRMS_API_KEY='your_key_here'"
echo ""

# 4. Vast.ai (for GPU training)
echo "4. VAST.AI (for foundation model fine-tuning)"
echo "   - Sign up: https://vast.ai/ (1 hour signup)"
echo "   - Add payment method (~$5 needed for P0011 full fine-tune)"
echo "   - Rent: A100 80GB @ \$1/hr (search 'A100' filter)"
echo "   - SSH into the rented machine"
echo "   - Run: git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay"
echo "   - Run: cd satellite-paraguay && pip install -r requirements.txt"
echo "   - Run: python3 scripts/train_p0011_full.py --epochs 30 --n-tiles 50 --device cuda"
echo ""

# 5. Adviser meeting
echo "5. ADVISER (Juan Carlos Cristaldo, FADA-UNA)"
echo "   - Schedule weekly 1-hour meeting"
echo "   - Show this ROAST.md first: 'Here's what I built, what do you think?'"
echo "   - Get approval on direction BEFORE submitting papers"
echo ""

# 6. IRB
echo "6. UNA IRB (for P0012 Yvy, P0031 Karamanu)"
echo "   - Email: comite.etica@rec.una.py"
echo "   - Tell them: 'Master thesis with indigenous community data, CARE Principles'"
echo "   - Timeline: 3-6 months"
echo ""

# 7. Email partners
echo "7. PARTNERS (use EMAIL_OUTREACH.md)"
echo "   - INFONA (P0011, P0010): INFONA@infona.gov.py"
echo "   - INDI (P0012): contacto@indi.gov.py"
echo "   - SENEPA (P0031): sene@mspbs.gov.py"
echo "   - Catastro: catastro@catastro.gov.py"
echo "   - FCM-UNA: fcm@med.una.py"
echo "   - MOPC: contacto@mopc.gov.py"
echo ""

# 8. Costs
echo "============================================================"
echo "ESTIMATED COSTS"
echo "============================================================"
echo "  Vast.ai GPU (P0011 Prithvi fine-tune): 4 hours × \$1/hr = \$4"
echo "  Vast.ai GPU (P0026 YOLOv8 training):   2 hours × \$1/hr = \$2"
echo "  Vast.ai GPU (P0012 LLaVA inference):   2 hours × \$1/hr = \$2"
echo "  Verra VCS API:                        free"
echo "  OpenAQ API:                           free (w/ key)"
echo "  NASA FIRMS API:                       free (w/ key)"
echo "  Google Earth Engine:                  free"
echo "  TOTAL:                                ~\$10"
echo ""
echo "============================================================"
echo "TIME ESTIMATES"
echo "============================================================"
echo "  Sign up for all 4 API accounts:      1 hour (parallel)"
echo "  Download 50 Sentinel-2 tiles:         30 minutes (after GEE auth)"
echo "  Run Prithvi fine-tune on GPU:        4 hours"
echo "  Re-run all 6 experiments:            2 hours"
echo "  Update paper.md with real metrics:  4 hours"
echo "  Submit to journals:                  1 hour (after 6 months of revisions)"
echo "  TOTAL:                                ~12 hours of work + 6 months wait"
echo ""
