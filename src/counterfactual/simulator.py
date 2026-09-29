"""
SIH26143 — Counterfactual Forward Drift Simulation Engine.
Tests the counterfactual hypothesis: "Assuming candidate vessel X discharged oil at timestamp T,
does simulated forward hydrodynamic transport reproduce the observed satellite slick geometry?"
Computes centroid error, Hausdorff distance, and spatial overlap (IoU).
"""

import math
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

from src.config.schemas import (
    SpillPolygon,
    MetoceanObservation,
    GeoPoint
)
from src.drift.lagrangian import LagrangianDriftEngine
from src.characterization.geometry import SlickGeometryExtractor


class CounterfactualSimulator:
    """Simulates forward oil drift from candidate vessel locations to test physical consistency."""

    def __init__(self, dt_seconds: float = 300.0):
        self.drift_engine = LagrangianDriftEngine(dt_seconds=dt_seconds)

    @classmethod
    def compute_modified_hausdorff_km(
        cls,
        pts_sim: List[Tuple[float, float]],
        pts_obs: List[Tuple[float, float]]
    ) -> float:
        """
        Computes Modified Hausdorff Distance (Dubuisson and Jain, 1994)
        between simulated particles and observed slick boundary points.
        """
        if not pts_sim or not pts_obs:
            return float("inf")

        # Directed distance d(sim -> obs)
        sum_d_sim = 0.0
        for s_lon, s_lat in pts_sim:
            min_d = min(
                SlickGeometryExtractor.haversine_distance_km(s_lat, s_lon, o_lat, o_lon)
                for o_lon, o_lat in pts_obs
            )
            sum_d_sim += min_d
        d_sim_to_obs = sum_d_sim / len(pts_sim)

        # Directed distance d(obs -> sim)
        sum_d_obs = 0.0
        for o_lon, o_lat in pts_obs:
            min_d = min(
                SlickGeometryExtractor.haversine_distance_km(o_lat, o_lon, s_lat, s_lon)
                for s_lon, s_lat in pts_sim
            )
            sum_d_obs += min_d
        d_obs_to_sim = sum_d_obs / len(pts_obs)

        return max(d_sim_to_obs, d_obs_to_sim)

    @classmethod
    def compute_bbox_iou(
        cls,
        sim_points: List[Tuple[float, float]],
        obs_ring: List[Tuple[float, float]]
    ) -> float:
        """Computes spatial bounding box Intersection-over-Union (IoU) in [0.0, 1.0]."""
        sim_lons = [p[0] for p in sim_points]
        sim_lats = [p[1] for p in sim_points]
        obs_lons = [p[0] for p in obs_ring]
        obs_lats = [p[1] for p in obs_ring]

        min_lon_s, max_lon_s = min(sim_lons), max(sim_lons)
        min_lat_s, max_lat_s = min(sim_lats), max(sim_lats)

        min_lon_o, max_lon_o = min(obs_lons), max(obs_lons)
        min_lat_o, max_lat_o = min(obs_lats), max(obs_lats)

        # Intersection bounds
        i_min_lon = max(min_lon_s, min_lon_o)
        i_max_lon = min(max_lon_s, max_lon_o)
        i_min_lat = max(min_lat_s, min_lat_o)
        i_max_lat = min(max_lat_s, max_lat_o)

        if i_max_lon <= i_min_lon or i_max_lat <= i_min_lat:
            return 0.0

        i_area = (i_max_lon - i_min_lon) * (i_max_lat - i_min_lat)
        s_area = (max_lon_s - min_lon_s) * (max_lat_s - min_lat_s)
        o_area = (max_lon_o - min_lon_o) * (max_lat_o - min_lat_o)

        union_area = s_area + o_area - i_area
        if union_area <= 0:
            return 0.0

        return min(1.0, max(0.0, i_area / union_area))

    def evaluate_counterfactual(
        self,
        candidate_release_coord: Tuple[float, float],  # (lon, lat)
        candidate_release_time: datetime,
        satellite_time: datetime,
        observed_spill: SpillPolygon,
        metocean: MetoceanObservation,
        num_particles: int = 60
    ) -> Dict[str, Any]:
        """
        Runs forward Lagrangian simulation from candidate coordinates to satellite time.
        Compares predicted plume with observed slick polygon.
        """
        duration_hours = (satellite_time - candidate_release_time).total_seconds() / 3600.0
        if duration_hours <= 0:
            return {
                "is_feasible": False,
                "error_reason": "Release timestamp is after satellite acquisition time",
                "counterfactual_score": 0.0
            }

        # Seed particles around candidate coordinate (simulating 10-minute continuous release)
        c_lon, c_lat = candidate_release_coord
        seed_points = [
            (c_lon + np.random.normal(0, 0.002), c_lat + np.random.normal(0, 0.002))
            for _ in range(num_particles)
        ]

        # Forward simulation (+dt)
        forward_sim = self.drift_engine.run_simulation(
            seed_points=seed_points,
            start_time=candidate_release_time,
            duration_hours=duration_hours,
            metocean=metocean,
            backward=False,
            random_seed=42
        )

        sim_term_pts = forward_sim["terminal_points"]
        sim_centroid = forward_sim["terminal_centroid"]
        obs_centroid = observed_spill.centroid

        # 1. Centroid distance error
        centroid_error_km = SlickGeometryExtractor.haversine_distance_km(
            sim_centroid["latitude"], sim_centroid["longitude"],
            obs_centroid.latitude, obs_centroid.longitude
        )

        # 2. Modified Hausdorff Distance
        obs_ring = observed_spill.coordinates[0]
        hausdorff_km = self.compute_modified_hausdorff_km(sim_term_pts, obs_ring)

        # 3. Spatial Bounding Box IoU
        iou = self.compute_bbox_iou(sim_term_pts, obs_ring)

        # 4. Composite Counterfactual Consistency Score in [0.0, 1.0]
        # Exponential penalty on centroid distance, boosted by IoU
        dist_factor = math.exp(-centroid_error_km / 4.0)
        cf_score = dist_factor * (0.4 + 0.6 * iou)
        cf_score = round(min(1.0, max(0.0, cf_score)), 3)

        survives_counterfactual = (centroid_error_km <= 5.0) and (cf_score >= 0.35)

        return {
            "is_feasible": True,
            "duration_hours": round(duration_hours, 2),
            "simulated_centroid": sim_centroid,
            "centroid_error_km": round(centroid_error_km, 3),
            "hausdorff_distance_km": round(hausdorff_km, 3),
            "bbox_iou": round(iou, 3),
            "counterfactual_consistency_score": cf_score,
            "survives_counterfactual": survives_counterfactual
        }
