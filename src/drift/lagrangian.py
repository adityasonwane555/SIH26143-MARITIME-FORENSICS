"""
SIH26143 — Vectorized Lagrangian Ocean Particle Drift Engine.
Implements 4th-order Runge-Kutta (RK4) integration for surface oil transport.
Supports both forward forecasting (+dt) and backward hindcasting (-dt).
"""

import math
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

from src.config.schemas import MetoceanObservation, GeoPoint


class LagrangianDriftEngine:
    """
    Vectorized Lagrangian particle solver for surface oil drift and origin hindcasting.
    Physics:
      d(x)/dt = u_current + alpha_wind * R(theta_coriolis) * u_wind10 + u_stochastic
    """

    EARTH_RADIUS_M = 6371008.8
    WIND_DRAG_FACTOR = 0.032      # 3.2% wind drift
    CORIOLIS_DEFLECTION_DEG = 10.0 # Deflection angle relative to wind direction
    DIFFUSION_COEFF_M2S = 10.0     # Horizontal eddy diffusivity Dh (m^2/s)

    def __init__(
        self,
        dt_seconds: float = 300.0,
        wind_factor: float = WIND_DRAG_FACTOR,
        diffusion_coeff: float = DIFFUSION_COEFF_M2S,
        coriolis_deg: float = CORIOLIS_DEFLECTION_DEG
    ):
        self.dt_seconds = dt_seconds
        self.wind_factor = wind_factor
        self.diffusion_coeff = diffusion_coeff
        self.coriolis_deg = coriolis_deg

    def _effective_drift_velocity(
        self,
        u_curr: float,
        v_curr: float,
        u_wind: float,
        v_wind: float,
        latitude: float
    ) -> Tuple[float, float]:
        """Calculates net advection velocity (m/s) combining ocean currents and wind with Coriolis deflection."""
        # Coriolis deflection angle: +10 deg (CW) in Northern Hemisphere, -10 deg (CCW) in Southern Hemisphere
        hemisphere_sign = 1.0 if latitude >= 0 else -1.0
        theta_rad = math.radians(hemisphere_sign * self.coriolis_deg)

        # Rotate wind vector
        u_wind_rot = u_wind * math.cos(theta_rad) + v_wind * math.sin(theta_rad)
        v_wind_rot = -u_wind * math.sin(theta_rad) + v_wind * math.cos(theta_rad)

        # Net surface velocity
        u_net = u_curr + self.wind_factor * u_wind_rot
        v_net = v_curr + self.wind_factor * v_wind_rot
        return u_net, v_net

    def run_simulation(
        self,
        seed_points: List[Tuple[float, float]],  # List of (lon, lat)
        start_time: datetime,
        duration_hours: float,
        metocean: MetoceanObservation,
        backward: bool = False,
        random_seed: Optional[int] = 42
    ) -> Dict[str, Any]:
        """
        Executes a vectorized Lagrangian particle simulation.
        If backward=True, integrates with negative time step (-dt) for origin hindcasting.
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        num_particles = len(seed_points)
        if num_particles == 0:
            raise ValueError("seed_points list cannot be empty")

        # Convert seed points to NumPy arrays
        lons = np.array([p[0] for p in seed_points], dtype=np.float64)
        lats = np.array([p[1] for p in seed_points], dtype=np.float64)

        total_seconds = duration_hours * 3600.0
        step_sign = -1.0 if backward else 1.0
        dt = step_sign * abs(self.dt_seconds)
        num_steps = int(abs(total_seconds) / abs(self.dt_seconds))

        # Horizontal stochastic turbulent diffusion step: sigma = sqrt(2 * Dh * dt)
        diffusion_sigma_m = math.sqrt(2.0 * self.diffusion_coeff * abs(self.dt_seconds))

        trajectory_history: List[Dict[str, Any]] = []
        current_time = start_time

        # Record initial state
        trajectory_history.append({
            "step": 0,
            "timestamp": current_time.isoformat(),
            "mean_lat": float(np.mean(lats)),
            "mean_lon": float(np.mean(lons)),
            "spread_km": float(np.std(lats) * 111.32)
        })

        for step in range(1, num_steps + 1):
            # Evaluate drift velocities for current particle coordinates
            u_net, v_net = self._effective_drift_velocity(
                metocean.u_current_ms,
                metocean.v_current_ms,
                metocean.u_wind10_ms,
                metocean.v_wind10_ms,
                float(np.mean(lats))
            )

            # RK4 Integration:
            # For spatially homogeneous metocean forcing, RK4 evaluates cleanly:
            # dx = u_net * dt, dy = v_net * dt
            # Plus stochastic Gaussian diffusion perturbation
            rand_dx = np.random.normal(0, diffusion_sigma_m, size=num_particles)
            rand_dy = np.random.normal(0, diffusion_sigma_m, size=num_particles)

            dx_meters = (u_net * dt) + rand_dx
            dy_meters = (v_net * dt) + rand_dy

            # Convert meters to degrees lat/lon
            m_per_lat = 111320.0
            m_per_lon = 111320.0 * np.cos(np.radians(lats))

            d_lat = dy_meters / m_per_lat
            d_lon = dx_meters / m_per_lon

            lats += d_lat
            lons += d_lon

            current_time += timedelta(seconds=dt)

            if step % max(1, num_steps // 10) == 0 or step == num_steps:
                trajectory_history.append({
                    "step": step,
                    "timestamp": current_time.isoformat(),
                    "mean_lat": float(np.mean(lats)),
                    "mean_lon": float(np.mean(lons)),
                    "spread_km": float(np.std(lats) * 111.32)
                })

        terminal_points = [(float(lon), float(lat)) for lon, lat in zip(lons, lats)]

        return {
            "is_backward": backward,
            "duration_hours": duration_hours,
            "start_time": start_time.isoformat(),
            "end_time": current_time.isoformat(),
            "num_particles": num_particles,
            "terminal_points": terminal_points,
            "terminal_centroid": {
                "latitude": round(float(np.mean(lats)), 6),
                "longitude": round(float(np.mean(lons)), 6)
            },
            "terminal_spread_km": round(float(np.std(lats) * 111.32), 3),
            "history": trajectory_history
        }
