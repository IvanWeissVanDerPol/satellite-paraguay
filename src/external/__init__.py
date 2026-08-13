"""External API clients — Verra, OpenAQ, Sentinel-5P, FIRMS, etc."""

from .verra_client import (
    compute_parcel_biomass,
    fetch_gold_standard_paraguay,
    fetch_verra_paraguay,
    verify_carbon_credit_real,
)

try:
    from .openaq_client import (  # noqa: F401
        aggregate_by_month,
        fetch_openaq_asuncion,
        fetch_openaq_for_location,
    )
except ImportError:
    pass

try:
    from .sentinel5p_client import (  # noqa: F401
        aggregate_atmospheric_by_month,
        fetch_sentinel5p_no2,
        fetch_sentinel5p_o3,
    )
except ImportError:
    pass

try:
    from .firms_client import (  # noqa: F401
        compute_fire_clusters,
        fetch_firms_fires,
    )
except ImportError:
    pass

__all__ = [
    "fetch_verra_paraguay",
    "fetch_gold_standard_paraguay",
    "verify_carbon_credit_real",
    "compute_parcel_biomass",
]
