"""FastAPI app exposing 6 paper pipelines as REST endpoints.

Run:
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

Endpoints:
    GET  /health                        — Health check
    POST /predict/deforestation         — P0011 Yvytu
    POST /predict/carbon                — P0100 Yvyra
    POST /predict/yield                 — P0025 Yrupe
    POST /predict/indigenous            — P0012 Yvy
    POST /predict/poaching              — P0026 Kai
    POST /predict/air-quality           — P0035 Tatakua
    GET  /info                          — API info
"""
from typing import Optional, List, Dict
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from src.papers.p0011_yvytu_deforestation import YvytuPipeline
from src.papers.p0100_yvyra_carbon_credits import YvyraPipeline
from src.papers.p0025_yrupe_yield import YrupePipeline
from src.papers.p0012_yvy_indigenous import YvyPipeline
from src.papers.p0026_kai_poaching import KaiPipeline
from src.papers.p0035_tatakua_air_quality import TatakuaPipeline


app = FastAPI(
    title="SatelliteCV-Paraguay API",
    description="REST API exposing 6 paper pipelines for multi-temporal earth observation of Paraguay",
    version="0.1.0",
)


# Request/response models
class TileRequest(BaseModel):
    tile_id: str = Field(..., description="Tile ID (lon_lat format)")
    bbox: Optional[Dict[str, float]] = None


class DeforestationRequest(BaseModel):
    tile_id: str
    ndvi_timeseries: List[List[float]] = Field(..., description="NDVI values (T, H*W)")
    dates: List[str]


class DeforestationResponse(BaseModel):
    tile_id: str
    deforestation_pixels: int
    total_pixels: int
    deforestation_fraction: float


class CarbonVerificationRequest(BaseModel):
    project_id: str
    tile_id: Optional[str] = None


class CarbonVerificationResponse(BaseModel):
    project_id: str
    verified: bool
    claimed_carbon_tons: float
    estimated_carbon_tons: float
    confidence: float


class YieldRequest(BaseModel):
    tile_id: str
    ndvi_series: List[float]


class YieldResponse(BaseModel):
    tile_id: str
    predicted_yield_tons_per_hectare: float


class PoachingRequest(BaseModel):
    tile_id: str
    image_path: Optional[str] = None


class PoachingResponse(BaseModel):
    tile_id: str
    num_detections: int


class AirQualityRequest(BaseModel):
    historical_pm25: List[float]
    days_ahead: int = 7


class AirQualityResponse(BaseModel):
    forecast_pm25: List[float]


# Health check
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "papers": [
            "P0011_yvytu",
            "P0100_yvyra",
            "P0025_yrupe",
            "P0012_yvy",
            "P0026_kai",
            "P0035_tatakua",
        ],
    }


@app.get("/info")
async def info():
    """API info."""
    return {
        "name": "SatelliteCV-Paraguay",
        "description": "Multi-temporal earth observation of Paraguay — 6 papers from one Python package",
        "version": "0.1.0",
        "endpoints": [
            "/health",
            "/info",
            "/predict/deforestation",
            "/predict/carbon",
            "/predict/yield",
            "/predict/indigenous",
            "/predict/poaching",
            "/predict/air-quality",
        ],
    }


# P0011 Yvytu
@app.post("/predict/deforestation", response_model=DeforestationResponse)
async def predict_deforestation(req: DeforestationRequest):
    """Detect deforestation in a Chaco tile."""
    pipeline = YvytuPipeline()
    try:
        import numpy as np
        T = len(req.dates)
        ndvi = np.array(req.ndvi_timeseries).reshape(T, -1)
        # Take first 256x256=65536 pixels
        if ndvi.shape[1] > 256 * 256:
            ndvi = ndvi[:, :256 * 256]
        H = W = int(ndvi.shape[1] ** 0.5)
        ndvi = ndvi.reshape(T, H, W)

        mask = pipeline.detect_deforestation(req.tile_id, ndvi, req.dates)
        return DeforestationResponse(
            tile_id=req.tile_id,
            deforestation_pixels=int(mask.sum()),
            total_pixels=int(mask.size),
            deforestation_fraction=float(mask.sum() / mask.size),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# P0100 Yvyra
@app.post("/predict/carbon", response_model=CarbonVerificationResponse)
async def predict_carbon(req: CarbonVerificationRequest):
    """Verify a carbon credit project."""
    pipeline = YvyraPipeline()
    try:
        result = pipeline.verify_carbon_credit(
            project_id=req.project_id,
            tile_id=req.tile_id,
        )
        return CarbonVerificationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# P0025 Yrupe
@app.post("/predict/yield", response_model=YieldResponse)
async def predict_yield(req: YieldRequest):
    """Predict soybean yield."""
    pipeline = YrupePipeline()
    try:
        import numpy as np
        ndvi = np.array(req.ndvi_series)
        pred = pipeline.predict_yield(req.tile_id, ndvi)
        return YieldResponse(
            tile_id=req.tile_id,
            predicted_yield_tons_per_hectare=float(pred),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# P0012 Yvy
@app.post("/predict/indigenous")
async def predict_indigenous(req: TileRequest):
    """Detect indigenous territory conflicts in a tile."""
    pipeline = YvyPipeline()
    try:
        pipeline.load_data()
        # Just return counts
        from src.parcel_analysis import get_indigenous_in_tile
        indigenous = get_indigenous_in_tile(req.bbox or {
            "min_lon": -62, "max_lon": -54,
            "min_lat": -27, "max_lat": -19,
        })
        return {
            "tile_id": req.tile_id,
            "indigenous_territories_count": len(indigenous),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# P0026 Kai
@app.post("/predict/poaching", response_model=PoachingResponse)
async def predict_poaching(req: PoachingRequest):
    """Detect poaching camps in Defensores del Chaco."""
    pipeline = KaiPipeline()
    try:
        # Stub — real impl requires image data
        return PoachingResponse(
            tile_id=req.tile_id,
            num_detections=0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# P0035 Tatakua
@app.post("/predict/air-quality", response_model=AirQualityResponse)
async def predict_air_quality(req: AirQualityRequest):
    """Forecast PM2.5 for Asunción."""
    pipeline = TatakuaPipeline()
    try:
        import numpy as np
        historical = np.array(req.historical_pm25)
        # Override forecast horizon
        pipeline.config["forecast_horizon_days"] = req.days_ahead
        forecast = pipeline.forecast_pm25(historical)
        return AirQualityResponse(
            forecast_pm25=[float(x) for x in forecast],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run with: uvicorn api.main:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
