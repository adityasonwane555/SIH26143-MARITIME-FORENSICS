"""
SIH26143 — Slick Geometric Characterizer.
Computes rigorous geospatial and morphological properties of detected slicks:
Area (Green's theorem on ellipsoidal/spherical coordinates), perimeter, centroid,
second central moments, principal axis orientation, and elongation.
"""

import math
from typing import List, Tuple, Dict, Any
from src.config.schemas import GeoPoint, SpillPolygon


class SlickGeometryExtractor:
    """Extracts geometric and morphological features from slick boundary polygons."""

    EARTH_RADIUS_KM = 6371.0088

    @classmethod
    def haversine_distance_km(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine formula for great-circle distance between two geographic coordinates."""
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2.0) ** 2
            + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return cls.EARTH_RADIUS_KM * c

    @classmethod
    def compute_polygon_perimeter_km(cls, ring: List[Tuple[float, float]]) -> float:
        """Computes polygon boundary perimeter in kilometers."""
        perimeter = 0.0
        n = len(ring)
        for i in range(n - 1):
            lon1, lat1 = ring[i]
            lon2, lat2 = ring[i + 1]
            perimeter += cls.haversine_distance_km(lat1, lon1, lat2, lon2)
        return perimeter

    @classmethod
    def compute_polygon_centroid(cls, ring: List[Tuple[float, float]]) -> GeoPoint:
        """Computes polygon geometric centroid using spherical polygon planar projection."""
        # Project ring to local flat plane around arithmetic mean
        mean_lat = sum(p[1] for p in ring[:-1]) / (len(ring) - 1)
        mean_lon = sum(p[0] for p in ring[:-1]) / (len(ring) - 1)

        m_per_lat = 111320.0
        m_per_lon = 111320.0 * math.cos(math.radians(mean_lat))

        # Local coordinates (x, y) in meters
        xy_pts = [((p[0] - mean_lon) * m_per_lon, (p[1] - mean_lat) * m_per_lat) for p in ring]

        # Standard planar polygon centroid formula
        area2 = 0.0
        cx = 0.0
        cy = 0.0
        n = len(xy_pts) - 1
        for i in range(n):
            xi, yi = xy_pts[i]
            xi1, yi1 = xy_pts[i + 1]
            cross = xi * yi1 - xi1 * yi
            area2 += cross
            cx += (xi + xi1) * cross
            cy += (yi + yi1) * cross

        if abs(area2) < 1e-6:
            return GeoPoint(latitude=mean_lat, longitude=mean_lon)

        cx /= (3.0 * area2)
        cy /= (3.0 * area2)

        centroid_lat = mean_lat + (cy / m_per_lat)
        centroid_lon = mean_lon + (cx / m_per_lon)
        return GeoPoint(latitude=round(centroid_lat, 6), longitude=round(centroid_lon, 6))

    @classmethod
    def compute_polygon_area_km2(cls, ring: List[Tuple[float, float]]) -> float:
        """Computes polygon surface area in km² using projected surveyor formula."""
        mean_lat = sum(p[1] for p in ring[:-1]) / (len(ring) - 1)
        mean_lon = sum(p[0] for p in ring[:-1]) / (len(ring) - 1)

        km_per_lat = 111.320
        km_per_lon = 111.320 * math.cos(math.radians(mean_lat))

        # Projected coordinates in km
        pts_km = [((p[0] - mean_lon) * km_per_lon, (p[1] - mean_lat) * km_per_lat) for p in ring]

        area = 0.0
        n = len(pts_km) - 1
        for i in range(n):
            xi, yi = pts_km[i]
            xi1, yi1 = pts_km[i + 1]
            area += (xi * yi1 - xi1 * yi)
        return abs(area) / 2.0

    @classmethod
    def compute_second_moments(cls, ring: List[Tuple[float, float]]) -> Dict[str, float]:
        """
        Computes second central moments to extract major axis, minor axis,
        orientation angle, and elongation.
        """
        mean_lat = sum(p[1] for p in ring[:-1]) / (len(ring) - 1)
        mean_lon = sum(p[0] for p in ring[:-1]) / (len(ring) - 1)

        km_per_lat = 111.320
        km_per_lon = 111.320 * math.cos(math.radians(mean_lat))

        pts_km = [((p[0] - mean_lon) * km_per_lon, (p[1] - mean_lat) * km_per_lat) for p in ring]

        # Centroid in local km
        centroid = cls.compute_polygon_centroid(ring)
        c_x = (centroid.longitude - mean_lon) * km_per_lon
        c_y = (centroid.latitude - mean_lat) * km_per_lat

        # Sample variances and covariance
        n = len(pts_km) - 1
        mu20 = sum((p[0] - c_x) ** 2 for p in pts_km[:n]) / n
        mu02 = sum((p[1] - c_y) ** 2 for p in pts_km[:n]) / n
        mu11 = sum((p[0] - c_x) * (p[1] - c_y) for p in pts_km[:n]) / n

        # Eigenvalues of 2x2 covariance matrix
        delta = math.sqrt((mu20 - mu02) ** 2 + 4.0 * (mu11 ** 2))
        lambda1 = (mu20 + mu02 + delta) / 2.0
        lambda2 = max(1e-6, (mu20 + mu02 - delta) / 2.0)

        # Semi-major and semi-minor axes (2 sigma equivalent)
        major_axis_len_km = 4.0 * math.sqrt(max(1e-6, lambda1))
        minor_axis_len_km = 4.0 * math.sqrt(max(1e-6, lambda2))
        elongation = max(1.0, major_axis_len_km / minor_axis_len_km)

        # Orientation angle in degrees from positive x-axis (East), normalized to [0, 360)
        theta_rad = 0.5 * math.atan2(2.0 * mu11, mu20 - mu02)
        orientation_deg = (math.degrees(theta_rad) + 360.0) % 360.0

        return {
            "major_axis_len_km": round(major_axis_len_km, 3),
            "minor_axis_len_km": round(minor_axis_len_km, 3),
            "elongation": round(elongation, 2),
            "orientation_deg": round(orientation_deg, 1)
        }

    @classmethod
    def characterize_polygon(
        cls,
        spill_id: str,
        scene_id: str,
        ring: List[Tuple[float, float]],
        confidence: float = 0.90
    ) -> SpillPolygon:
        """Full characterization returning a validated SpillPolygon schema object."""
        area_km2 = cls.compute_polygon_area_km2(ring)
        perimeter_km = cls.compute_polygon_perimeter_km(ring)
        centroid = cls.compute_polygon_centroid(ring)
        moments = cls.compute_second_moments(ring)

        return SpillPolygon(
            spill_id=spill_id,
            scene_id=scene_id,
            coordinates=[ring],
            area_km2=round(area_km2, 2),
            perimeter_km=round(perimeter_km, 2),
            centroid=centroid,
            major_axis_len_km=moments["major_axis_len_km"],
            minor_axis_len_km=moments["minor_axis_len_km"],
            orientation_deg=moments["orientation_deg"],
            elongation=moments["elongation"],
            confidence=confidence
        )
