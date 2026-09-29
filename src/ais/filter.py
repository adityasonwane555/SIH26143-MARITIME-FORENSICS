"""
SIH26143 — AIS Spatiotemporal Corridor Filtering Engine.
Filters large vessel catalogs to identify candidate ships whose historical trajectories
intersect the estimated origin probability envelope during the inferred release window.
"""

import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from src.config.schemas import AISTrack, OriginProbabilityGrid, GeoPoint
from src.characterization.geometry import SlickGeometryExtractor


class AISCorridorFilter:
    """Spatiotemporal candidate filtering of AIS vessel tracks."""

    @classmethod
    def filter_candidates(
        cls,
        tracks: List[AISTrack],
        origin_grid: OriginProbabilityGrid,
        spatial_buffer_km: float = 15.0,
        temporal_buffer_hours: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Filters vessel tracks against the origin probability envelope and release window.
        Returns a list of candidate vessels with proximity and compatibility metrics.
        """
        candidates: List[Dict[str, Any]] = []

        t_min = origin_grid.estimated_release_window[0] - timedelta(hours=temporal_buffer_hours)
        t_max = origin_grid.estimated_release_window[1] + timedelta(hours=temporal_buffer_hours)

        # Buffer in degrees
        deg_buffer = spatial_buffer_km / 111.32
        bbox = origin_grid.bounds
        b_min_lat = bbox.min_lat - deg_buffer
        b_max_lat = bbox.max_lat + deg_buffer
        b_min_lon = bbox.min_lon - deg_buffer
        b_max_lon = bbox.max_lon + deg_buffer

        origin_centroid = origin_grid.estimated_centroid

        for track in tracks:
            # 1. Quick Spatial & Temporal check across track points
            relevant_pts = [
                p for p in track.points
                if t_min <= p.timestamp <= t_max
                and b_min_lat <= p.latitude <= b_max_lat
                and b_min_lon <= p.longitude <= b_max_lon
            ]

            if not relevant_pts:
                continue

            # 2. Detailed distance to origin centroid
            min_dist_km = float("inf")
            best_point = relevant_pts[0]

            for p in relevant_pts:
                dist = SlickGeometryExtractor.haversine_distance_km(
                    p.latitude, p.longitude,
                    origin_centroid.latitude, origin_centroid.longitude
                )
                if dist < min_dist_km:
                    min_dist_km = dist
                    best_point = p

            # 3. Sample origin probability surface at vessel closest point
            # Map lat/lon to grid indices
            p_lat = best_point.latitude
            p_lon = best_point.longitude

            prob_val = 0.0
            matrix = origin_grid.probability_matrix
            rows = len(matrix)
            cols = len(matrix[0]) if rows > 0 else 0

            if rows > 0 and cols > 0 and bbox.min_lat <= p_lat <= bbox.max_lat and bbox.min_lon <= p_lon <= bbox.max_lon:
                r_idx = int((p_lat - bbox.min_lat) / (bbox.max_lat - bbox.min_lat) * (rows - 1))
                c_idx = int((p_lon - bbox.min_lon) / (bbox.max_lon - bbox.min_lon) * (cols - 1))
                r_idx = min(rows - 1, max(0, r_idx))
                c_idx = min(cols - 1, max(0, c_idx))
                prob_val = matrix[r_idx][c_idx]

            candidates.append({
                "mmsi": track.mmsi,
                "vessel_name": track.vessel_name,
                "vessel_type": track.vessel_type,
                "min_distance_km": round(min_dist_km, 3),
                "closest_point": {
                    "timestamp": best_point.timestamp.isoformat(),
                    "latitude": best_point.latitude,
                    "longitude": best_point.longitude,
                    "sog_knots": best_point.sog_knots,
                    "cog_degrees": best_point.cog_degrees
                },
                "origin_probability_density": float(prob_val),
                "has_ais_gaps": track.has_gaps,
                "max_gap_minutes": track.max_gap_minutes,
                "track_quality_score": track.quality_score,
                "total_points_in_window": len(relevant_pts)
            })

        # Sort candidates by minimum distance ascending
        candidates.sort(key=lambda c: c["min_distance_km"])
        return candidates
