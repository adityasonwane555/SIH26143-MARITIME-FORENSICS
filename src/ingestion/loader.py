"""
SIH26143 — Data Ingestion and Validation Engine.
Loads satellite slick polygons, metocean hydrodynamic grids, and AIS vessel tracks.
Enforces Pydantic schema validation and provenance tracking.
"""

import csv
import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from src.config.schemas import (
    SpillPolygon,
    MetoceanObservation,
    AISPoint,
    AISTrack,
    BoundingBox,
    GeoPoint,
)


class ForensicDataLoader:
    """Robust data loader for maritime forensic investigation assets."""

    @staticmethod
    def load_slick_geojson(filepath: str) -> SpillPolygon:
        """Loads and validates a detected oil slick GeoJSON polygon."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Slick GeoJSON file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        if not features:
            raise ValueError(f"GeoJSON contains no features: {filepath}")

        feat = features[0]
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})

        if geom.get("type") != "Polygon":
            raise ValueError(f"Expected geometry type 'Polygon', got {geom.get('type')}")

        coords = geom.get("coordinates", [])
        if not coords or not coords[0]:
            raise ValueError("Polygon coordinates are empty")

        centroid_raw = props.get("centroid", {})
        centroid = GeoPoint(
            latitude=centroid_raw.get("latitude", 0.0),
            longitude=centroid_raw.get("longitude", 0.0)
        )

        return SpillPolygon(
            spill_id=props.get("spill_id", "UNKNOWN_SPILL"),
            scene_id=props.get("scene_id", "UNKNOWN_SCENE"),
            coordinates=coords,
            area_km2=float(props.get("area_km2", 0.0)),
            perimeter_km=float(props.get("perimeter_km", 0.0)),
            centroid=centroid,
            major_axis_len_km=float(props.get("major_axis_len_km", 1.0)),
            minor_axis_len_km=float(props.get("minor_axis_len_km", 1.0)),
            orientation_deg=float(props.get("orientation_deg", 0.0)),
            elongation=float(props.get("elongation", 1.0)),
            confidence=float(props.get("confidence", 0.5)),
        )

    @staticmethod
    def load_metocean_json(filepath: str) -> MetoceanObservation:
        """Loads and validates metocean wind and current observations."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Metocean JSON not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        bounds_raw = data.get("bounds", {})
        bounds = BoundingBox(
            min_lat=bounds_raw.get("min_lat", -90.0),
            max_lat=bounds_raw.get("max_lat", 90.0),
            min_lon=bounds_raw.get("min_lon", -180.0),
            max_lon=bounds_raw.get("max_lon", 180.0),
        )

        ts_str = data.get("timestamp")
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00")) if ts_str else datetime.now(timezone.utc)

        u_curr = float(data.get("u_current_ms") or data.get("current_u_mps") or data.get("u_current") or 0.0)
        v_curr = float(data.get("v_current_ms") or data.get("current_v_mps") or data.get("v_current") or 0.0)
        u_wind = float(data.get("u_wind10_ms") or data.get("wind_u_mps") or data.get("u_wind") or 0.0)
        v_wind = float(data.get("v_wind10_ms") or data.get("wind_v_mps") or data.get("v_wind") or 0.0)

        return MetoceanObservation(
            timestamp=ts,
            grid_bounds=bounds,
            u_current_ms=u_curr,
            v_current_ms=v_curr,
            u_wind10_ms=u_wind,
            v_wind10_ms=v_wind,
            sea_surface_temp_c=data.get("sea_surface_temp_c"),
            wave_height_m=data.get("wave_height_m"),
            source=data.get("source", "UNKNOWN")
        )

    @staticmethod
    def load_ais_csv(filepath: str) -> List[AISTrack]:
        """Loads historical AIS transmissions from CSV and segments into per-vessel tracks."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"AIS CSV not found: {filepath}")

        tracks_by_mmsi: Dict[str, Dict[str, Any]] = {}

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Support both uppercase and lowercase column variants
                mmsi_raw = row.get("MMSI") or row.get("mmsi")
                if not mmsi_raw:
                    continue
                mmsi = str(mmsi_raw).strip()

                vessel_name = str(row.get("VesselName") or row.get("vessel_name") or "UNKNOWN").strip()
                vessel_type = str(row.get("VesselType") or row.get("vessel_type") or "Cargo").strip()

                ts_str = row.get("Timestamp") or row.get("timestamp")
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

                lat = float(row.get("Latitude") or row.get("latitude") or 0.0)
                lon = float(row.get("Longitude") or row.get("longitude") or 0.0)
                sog = float(row.get("SOG") or row.get("sog_knots") or row.get("sog") or 0.0)
                cog = float(row.get("COG") or row.get("cog_degrees") or row.get("cog") or 0.0)
                heading_val = row.get("Heading") or row.get("heading") or cog

                pt = AISPoint(
                    timestamp=ts,
                    latitude=lat,
                    longitude=lon,
                    sog_knots=sog,
                    cog_degrees=cog,
                    heading=float(heading_val)
                )

                if mmsi not in tracks_by_mmsi:
                    tracks_by_mmsi[mmsi] = {
                        "mmsi": mmsi,
                        "vessel_name": vessel_name,
                        "vessel_type": vessel_type,
                        "points": []
                    }
                tracks_by_mmsi[mmsi]["points"].append(pt)


        # Build AISTrack objects and analyze continuity
        track_list: List[AISTrack] = []
        for mmsi, track_dict in tracks_by_mmsi.items():
            pts = sorted(track_dict["points"], key=lambda p: p.timestamp)
            max_gap_m = 0.0
            has_gaps = False

            for i in range(1, len(pts)):
                gap_sec = (pts[i].timestamp - pts[i - 1].timestamp).total_seconds()
                gap_min = gap_sec / 60.0
                if gap_min > max_gap_m:
                    max_gap_m = gap_min
                if gap_min > 90.0:  # Gap exceeding 1.5 hours in open water
                    has_gaps = True

            quality = 1.0
            if has_gaps:
                quality = max(0.2, 1.0 - (max_gap_m / 600.0))

            track_list.append(
                AISTrack(
                    mmsi=mmsi,
                    vessel_name=track_dict["vessel_name"],
                    vessel_type=track_dict["vessel_type"],
                    points=pts,
                    has_gaps=has_gaps,
                    max_gap_minutes=round(max_gap_m, 1),
                    quality_score=round(quality, 2)
                )
            )

        return track_list

    @staticmethod
    def load_case_catalog(filepath: str = "data/metadata/cases.csv") -> List[Dict[str, Any]]:
        """Loads and returns the catalog of historical and benchmark cases."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Case catalog not found: {filepath}")

        cases = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cases.append(row)
        return cases
