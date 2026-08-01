"""satellite-paraguay — Multi-temporal earth observation of Paraguay.

Sub-modules:
- satellite_io: Sentinel-2 / Landsat / Planet download + preprocessing
- paraguay_admin: 18 deptos + 268 distritos + 7,912 tiles
- foundation_models: Prithvi (IBM-NASA), AlphaEarth (Google), DINOv2 (Meta)
- parcel_analysis: Catastro intersection + buffer
- timeseries: Multi-temporal stacking + change detection
- evaluation: F1/IoU/mAP metrics + benchmarks
- papers: One folder per paper (6 papers)
"""

__version__ = "0.1.0"
__author__ = "Iván Weiss Van der Pol"
__email__ = "ivan@example.com"
