"""
SIH26143 — Core Data Models and Pydantic Schemas.
Strictly typed data contracts across all pipeline stages.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, field_validator


class DirectionEnum(str, Enum):
    SUPPORTS = "supports"
    REFUTES = "refutes"
    NEUTRAL = "neutral"


class HypothesisType(str, Enum):
    VESSEL = "vessel"
    OFFSHORE_INFRASTRUCTURE = "offshore_infrastructure"
    NATURAL_SEEP = "natural_seep"
    DARK_VESSEL = "dark_vessel"
    FALSE_POSITIVE = "false_positive"


class AttributionDecision(str, Enum):
    ATTRIBUTED = "attributed"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    NON_VESSEL_SOURCE = "non_vessel_source"
    FALSE_POSITIVE = "false_positive"


class GeoPoint(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")


class BoundingBox(BaseModel):
    min_lat: float = Field(..., ge=-90.0, le=90.0)
    max_lat: float = Field(..., ge=-90.0, le=90.0)
    min_lon: float = Field(..., ge=-180.0, le=180.0)
    max_lon: float = Field(..., ge=-180.0, le=180.0)

    @field_validator("max_lat")
    @classmethod
    def lat_order(cls, v: float, info):
        if "min_lat" in info.data and v < info.data["min_lat"]:
            raise ValueError("max_lat must be >= min_lat")
        return v

    @field_validator("max_lon")
    @classmethod
    def lon_order(cls, v: float, info):
        if "min_lon" in info.data and v < info.data["min_lon"]:
            raise ValueError("max_lon must be >= min_lon")
        return v


class SatelliteScene(BaseModel):
    scene_id: str
    sensor: str = Field("Sentinel-1 SAR", description="Satellite sensor name")
    acquisition_time: datetime
    bounds: BoundingBox
    polarization: str = "VV+VH"
    resolution_m: float = 10.0
    mean_backscatter_db: Optional[float] = None
    lookalike_risk_score: float = Field(0.0, ge=0.0, le=1.0)
    provenance: Dict[str, Any] = Field(default_factory=dict)
    is_synthetic: bool = False


class SpillPolygon(BaseModel):
    spill_id: str
    scene_id: str
    coordinates: List[List[Tuple[float, float]]] = Field(
        ..., description="List of polygon linear rings [(lon, lat), ...]"
    )
    area_km2: float = Field(..., ge=0.0)
    perimeter_km: float = Field(..., ge=0.0)
    centroid: GeoPoint
    major_axis_len_km: float = Field(..., ge=0.0)
    minor_axis_len_km: float = Field(..., ge=0.0)
    orientation_deg: float = Field(..., ge=0.0, le=360.0)
    elongation: float = Field(..., ge=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    estimated_age_hours: Optional[Tuple[float, float]] = None


class MetoceanObservation(BaseModel):
    timestamp: datetime
    grid_bounds: BoundingBox
    u_current_ms: float = Field(..., description="Eastward ocean current velocity in m/s")
    v_current_ms: float = Field(..., description="Northward ocean current velocity in m/s")
    u_wind10_ms: float = Field(..., description="Eastward 10m wind velocity in m/s")
    v_wind10_ms: float = Field(..., description="Northward 10m wind velocity in m/s")
    sea_surface_temp_c: Optional[float] = None
    wave_height_m: Optional[float] = None
    source: str = "CMEMS/ERA5"


class AISPoint(BaseModel):
    timestamp: datetime
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    sog_knots: float = Field(..., ge=0.0, le=60.0, description="Speed Over Ground in knots")
    cog_degrees: float = Field(..., ge=0.0, le=360.0, description="Course Over Ground in degrees")
    heading: Optional[float] = None


class AISTrack(BaseModel):
    mmsi: str
    vessel_name: str = "UNKNOWN"
    vessel_type: str = "Cargo"
    imo: Optional[str] = None
    callsign: Optional[str] = None
    points: List[AISPoint] = Field(default_factory=list)
    total_distance_km: float = 0.0
    has_gaps: bool = False
    max_gap_minutes: float = 0.0
    quality_score: float = Field(1.0, ge=0.0, le=1.0)


class OriginProbabilityGrid(BaseModel):
    grid_id: str
    timestamp_evaluated: datetime
    bounds: BoundingBox
    resolution_lat: float
    resolution_lon: float
    probability_matrix: List[List[float]] = Field(..., description="2D normalized probability density")
    estimated_centroid: GeoPoint
    estimated_release_window: Tuple[datetime, datetime]
    contour_geojson: Optional[Dict[str, Any]] = None


class EvidenceItem(BaseModel):
    evidence_id: str
    hypothesis_id: str
    type: str = Field(..., description="e.g. trajectory_consistency, speed_compatibility")
    value: float = Field(..., ge=0.0, le=1.0)
    direction: DirectionEnum
    source: str = Field(..., description="e.g. AIS, Metocean, SAR")
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str
    timestamp_evaluated: datetime = Field(default_factory=datetime.utcnow)


class FalsificationResult(BaseModel):
    hypothesis_id: str
    survives: bool
    challenges_passed: int
    challenges_failed: int
    contradicting_reasons: List[str] = Field(default_factory=list)
    counterfactual_iou: Optional[float] = None
    counterfactual_hausdorff_km: Optional[float] = None


class Hypothesis(BaseModel):
    hypothesis_id: str
    type: HypothesisType
    subject_id: str = Field(..., description="MMSI, Infrastructure ID, or 'UNKNOWN'")
    subject_name: str
    prior_probability: float = Field(..., ge=0.0, le=1.0)
    posterior_probability: float = Field(0.0, ge=0.0, le=1.0)
    supporting_evidence: List[EvidenceItem] = Field(default_factory=list)
    contradicting_evidence: List[EvidenceItem] = Field(default_factory=list)
    falsification: Optional[FalsificationResult] = None
    is_falsified: bool = False


class NextEvidenceRecommendation(BaseModel):
    recommendation_id: str
    action_type: str = Field(..., description="e.g. SAR_REVISIT, OPTICAL_TASKING, AERIAL_PATROL")
    target_sector: BoundingBox
    separates_hypotheses: Tuple[str, str]
    expected_information_gain_bits: float = Field(..., ge=0.0)
    rationale: str
    urgency: str = "Medium"


class ForensicDossier(BaseModel):
    incident_id: str
    title: str
    incident_time: datetime
    location: GeoPoint
    decision: AttributionDecision
    leading_hypothesis_id: Optional[str] = None
    leading_subject_name: Optional[str] = None
    attribution_confidence: float = Field(0.0, ge=0.0, le=1.0)
    entropy_bits: float
    is_abstention: bool = False
    abstention_reason: Optional[str] = None
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    origin_estimate: Optional[OriginProbabilityGrid] = None
    detected_slick: Optional[SpillPolygon] = None
    recommended_evidence: List[NextEvidenceRecommendation] = Field(default_factory=list)
    audit_trail: Dict[str, Any] = Field(default_factory=dict)
