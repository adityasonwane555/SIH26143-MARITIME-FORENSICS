"""
SIH26143 — Baseline Attribution Pipeline.
Implements the standard heuristic attribution baseline:
Satellite -> Detection -> Backward Drift -> Origin Envelope -> AIS Corridor Filter -> Heuristic Vessel Ranking.
Used as the control reference to measure the empirical value of our advanced forensic innovations.
"""

import math
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional

from src.config.schemas import (
    SpillPolygon,
    MetoceanObservation,
    AISTrack,
    OriginProbabilityGrid,
    GeoPoint
)
from src.drift.lagrangian import LagrangianDriftEngine
from src.drift.origin_surface import OriginSurfaceEstimator
from src.ais.filter import AISCorridorFilter
from src.characterization.geometry import SlickGeometryExtractor


class BaselineAttributionPipeline:
    """
    Standard linear attribution baseline.
    Uses heuristic distance, temporal compatibility, and track orientation weights.
    """

    def __init__(
        self,
        weight_distance: float = 0.40,
        weight_time: float = 0.30,
        weight_course: float = 0.15,
        weight_origin_prob: float = 0.15
    ):
        self.w_d = weight_distance
        self.w_t = weight_time
        self.w_c = weight_course
        self.w_p = weight_origin_prob
        self.drift_engine = LagrangianDriftEngine(dt_seconds=300.0)

    def run(
        self,
        spill: SpillPolygon,
        metocean: MetoceanObservation,
        tracks: List[AISTrack],
        hindcast_hours: float = 6.0,
        num_seed_particles: int = 100
    ) -> Dict[str, Any]:
        """Executes the end-to-end baseline pipeline."""
        start_time = datetime.now(timezone.utc)

        # 1. Sample seed points along the slick polygon boundary
        ring = spill.coordinates[0]
        n_pts = len(ring)
        step = max(1, n_pts // num_seed_particles)
        seed_points = [ring[i] for i in range(0, n_pts, step)]
        if len(seed_points) > num_seed_particles:
            seed_points = seed_points[:num_seed_particles]

        # 2. Run backward Lagrangian hindcast (-dt)
        sat_time = metocean.timestamp
        sim_result = self.drift_engine.run_simulation(
            seed_points=seed_points,
            start_time=sat_time,
            duration_hours=hindcast_hours,
            metocean=metocean,
            backward=True,
            random_seed=42
        )

        # 3. Estimate continuous Origin Probability Surface P(x, y)
        release_window_start = sat_time - timedelta(hours=hindcast_hours)
        origin_grid = OriginSurfaceEstimator.estimate_surface(
            terminal_points=sim_result["terminal_points"],
            start_time=release_window_start,
            end_time=sat_time,
            grid_resolution=40
        )

        # 4. Spatiotemporal AIS candidate filtering
        filtered_candidates = AISCorridorFilter.filter_candidates(
            tracks=tracks,
            origin_grid=origin_grid,
            spatial_buffer_km=20.0,
            temporal_buffer_hours=2.0
        )

        # 5. Compute transparent heuristic scores for each candidate
        ranked_vessels = []
        c_lat = origin_grid.estimated_centroid.latitude
        c_lon = origin_grid.estimated_centroid.longitude

        for cand in filtered_candidates:
            d_km = cand["min_distance_km"]
            # Distance score: exponential decay with half-life at 10 km
            s_dist = math.exp(-d_km / 10.0)

            # Time compatibility: delta from release window mid-point
            pt_ts = datetime.fromisoformat(cand["closest_point"]["timestamp"])
            mid_release = release_window_start + timedelta(hours=hindcast_hours / 2.0)
            delta_t_hours = abs((pt_ts - mid_release).total_seconds()) / 3600.0
            s_time = math.exp(-delta_t_hours / 3.0)

            # Course alignment with slick elongation orientation
            cog_deg = cand["closest_point"]["cog_degrees"]
            diff_rad = math.radians(abs(cog_deg - spill.orientation_deg))
            s_course = max(0.0, math.cos(diff_rad))

            # Origin probability density
            # Scale density so max expected is ~1.0
            s_prob = min(1.0, cand["origin_probability_density"] * 100.0)

            # Total weighted heuristic score
            total_score = (
                self.w_d * s_dist
                + self.w_t * s_time
                + self.w_c * s_course
                + self.w_p * s_prob
            )

            ranked_vessels.append({
                "mmsi": cand["mmsi"],
                "vessel_name": cand["vessel_name"],
                "vessel_type": cand["vessel_type"],
                "baseline_score": round(total_score, 4),
                "min_distance_km": cand["min_distance_km"],
                "delta_t_hours": round(delta_t_hours, 2),
                "closest_point": cand["closest_point"],
                "feature_breakdown": {
                    "distance_score": round(s_dist, 3),
                    "time_score": round(s_time, 3),
                    "course_score": round(s_course, 3),
                    "origin_prob_score": round(s_prob, 3)
                }
            })

        # Sort by total score descending
        ranked_vessels.sort(key=lambda v: v["baseline_score"], reverse=True)

        exec_time_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0

        top_candidate = ranked_vessels[0] if ranked_vessels else None

        return {
            "pipeline": "BASELINE_HEURISTIC",
            "execution_time_ms": round(exec_time_ms, 2),
            "spill_id": spill.spill_id,
            "origin_centroid": {
                "latitude": round(c_lat, 6),
                "longitude": round(c_lon, 6)
            },
            "hindcast_hours": hindcast_hours,
            "origin_grid": origin_grid,
            "total_candidates_evaluated": len(ranked_vessels),
            "top_candidate": top_candidate,
            "ranked_vessels": ranked_vessels
        }
