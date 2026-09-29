"""
SIH26143 — Origin Probability Surface Generator.
Transforms terminal backward Lagrangian particle positions into a continuous
2D Kernel Density Estimation (KDE) probability grid and GeoJSON contours.
"""

import math
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

from src.config.schemas import (
    OriginProbabilityGrid,
    BoundingBox,
    GeoPoint
)


class OriginSurfaceEstimator:
    """Generates 2D origin probability surfaces from backtracked particles."""

    @classmethod
    def estimate_surface(
        cls,
        terminal_points: List[Tuple[float, float]],  # List of (lon, lat)
        start_time: datetime,
        end_time: datetime,
        grid_resolution: int = 50,
        margin_factor: float = 0.25
    ) -> OriginProbabilityGrid:
        """
        Fits a 2D Gaussian KDE to terminal particle positions and evaluates on a regular grid.
        Returns a normalized OriginProbabilityGrid with GeoJSON contours.
        """
        if len(terminal_points) < 5:
            raise ValueError("At least 5 terminal points required to estimate origin probability surface.")

        lons = np.array([p[0] for p in terminal_points], dtype=np.float64)
        lats = np.array([p[1] for p in terminal_points], dtype=np.float64)

        mean_lat = float(np.mean(lats))
        mean_lon = float(np.mean(lons))
        std_lat = max(1e-4, float(np.std(lats)))
        std_lon = max(1e-4, float(np.std(lons)))

        # Define grid bounds with margin
        span_lat = max(0.05, (np.max(lats) - np.min(lats)) * (1.0 + margin_factor))
        span_lon = max(0.05, (np.max(lons) - np.min(lons)) * (1.0 + margin_factor))

        min_lat = mean_lat - span_lat / 2.0
        max_lat = mean_lat + span_lat / 2.0
        min_lon = mean_lon - span_lon / 2.0
        max_lon = mean_lon + span_lon / 2.0

        grid_lats = np.linspace(min_lat, max_lat, grid_resolution)
        grid_lons = np.linspace(min_lon, max_lon, grid_resolution)

        # Vectorized 2D Gaussian KDE evaluation
        # Bandwidth selection (Silverman's rule of thumb)
        n = len(terminal_points)
        h_lat = 1.06 * std_lat * (n ** (-0.2))
        h_lon = 1.06 * std_lon * (n ** (-0.2))

        # Meshgrid (rows = lat, cols = lon)
        lon_mesh, lat_mesh = np.meshgrid(grid_lons, grid_lats)

        # Compute density sum over all particles
        density_matrix = np.zeros((grid_resolution, grid_resolution), dtype=np.float64)
        for p_lon, p_lat in terminal_points:
            z_lon = (lon_mesh - p_lon) / h_lon
            z_lat = (lat_mesh - p_lat) / h_lat
            density_matrix += np.exp(-0.5 * (z_lon ** 2 + z_lat ** 2))

        # Normalize matrix so total sum is 1.0
        total_mass = np.sum(density_matrix)
        if total_mass > 0:
            density_matrix /= total_mass

        # Generate simplified GeoJSON contours for 50%, 80%, and 95% confidence intervals
        sorted_densities = np.sort(density_matrix.flatten())[::-1]
        cumulative_mass = np.cumsum(sorted_densities)

        # Threshold densities
        idx_50 = np.searchsorted(cumulative_mass, 0.50)
        idx_80 = np.searchsorted(cumulative_mass, 0.80)
        idx_95 = min(len(sorted_densities) - 1, np.searchsorted(cumulative_mass, 0.95))

        thresh_50 = float(sorted_densities[idx_50]) if idx_50 < len(sorted_densities) else 0.0
        thresh_80 = float(sorted_densities[idx_80]) if idx_80 < len(sorted_densities) else 0.0
        thresh_95 = float(sorted_densities[idx_95])

        # Generate contour bounding polygons
        contour_features = []
        for level_name, thresh in [("50% Confidence Origin", thresh_50), ("80% Confidence Origin", thresh_80), ("95% Confidence Origin", thresh_95)]:
            mask = density_matrix >= thresh
            if np.any(mask):
                y_idx, x_idx = np.where(mask)
                c_min_lat = float(grid_lats[np.min(y_idx)])
                c_max_lat = float(grid_lats[np.max(y_idx)])
                c_min_lon = float(grid_lons[np.min(x_idx)])
                c_max_lon = float(grid_lons[np.max(x_idx)])

                contour_ring = [
                    [c_min_lon, c_min_lat],
                    [c_max_lon, c_min_lat],
                    [c_max_lon, c_max_lat],
                    [c_min_lon, c_max_lat],
                    [c_min_lon, c_min_lat]
                ]
                contour_features.append({
                    "type": "Feature",
                    "properties": {"level": level_name, "threshold": round(thresh, 6)},
                    "geometry": {"type": "Polygon", "coordinates": [contour_ring]}
                })

        contour_geojson = {
            "type": "FeatureCollection",
            "features": contour_features
        }

        bbox = BoundingBox(
            min_lat=round(min_lat, 6),
            max_lat=round(max_lat, 6),
            min_lon=round(min_lon, 6),
            max_lon=round(max_lon, 6)
        )

        now_utc = datetime.now(timezone.utc)
        return OriginProbabilityGrid(
            grid_id=f"ORIGIN_GRID_{int(now_utc.timestamp())}",
            timestamp_evaluated=now_utc,
            bounds=bbox,
            resolution_lat=round((max_lat - min_lat) / grid_resolution, 6),
            resolution_lon=round((max_lon - min_lon) / grid_resolution, 6),
            probability_matrix=density_matrix.tolist(),
            estimated_centroid=GeoPoint(latitude=round(mean_lat, 6), longitude=round(mean_lon, 6)),
            estimated_release_window=(start_time, end_time),
            contour_geojson=contour_geojson
        )
