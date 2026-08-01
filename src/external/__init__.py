"""External API clients — Verra, OpenAQ, Sentinel-5P, FIRMS, etc."""
from .verra_client import (
    fetch_verra_paraguay,
    fetch_gold_standard_paraguay,
    verify_carbon_credit_real,
    compute_parcel_biomass,
)

try:
    from .openaq_client import (
        fetch_openaq_asuncion,
        fetch_openaq_for_location,
        aggregate_by_month,
    )
except ImportError:
    pass

try:
    from .sentinel5p_client import (
        fetch_sentinel5p_no2,
        fetch_sentinel5p_o3,
        aggregate_atmospheric_by_month,
    )
except ImportError:
    pass

try:
    from .firms_client import (
        fetch_firms_fires,
        compute_fire_clusters,
    )
except ImportError:
    pass

__all__ = [
    "fetch_verra_paraguay",
    "fetch_gold_standard_paraguay",
    "verify_carbon_credit_real",
    "compute_parcel_biomass",
]
