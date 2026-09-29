"""
SIH26143 — Analytical Synthetic Benchmark Scenario Generator.
Generates CASE_005_SYNTHETIC_CHALLENGE with exact mathematical ground-truth.
Used for deterministic regression tests, adversarial challenge verification, and baselines.
"""

import json
import math
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any


def generate_benchmark_scenario(output_dir: str = "data/synthetic") -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)

    # 1. Temporal Reference Window
    t_start = datetime(2024, 5, 10, 6, 0, 0, tzinfo=timezone.utc)
    t_release_true = datetime(2024, 5, 10, 10, 0, 0, tzinfo=timezone.utc)
    t_sat = datetime(2024, 5, 10, 16, 0, 0, tzinfo=timezone.utc)  # 6h post-release
    t_end = datetime(2024, 5, 10, 20, 0, 0, tzinfo=timezone.utc)

    # 2. Metocean Hydrodynamic Forcing
    # Constant surface current & wind for analytical tractability
    u_current = 0.25   # m/s eastward
    v_current = -0.15  # m/s southward
    u_wind10 = 4.0     # m/s eastward
    v_wind10 = -3.0    # m/s southward
    wind_drag = 0.032  # 3.2% wind factor

    net_u_drift = u_current + wind_drag * u_wind10  # 0.25 + 0.128 = 0.378 m/s
    net_v_drift = v_current + wind_drag * v_wind10  # -0.15 - 0.096 = -0.246 m/s

    # Metocean grid metadata
    metocean_data = {
        "timestamp": t_sat.isoformat(),
        "bounds": {"min_lat": 15.0, "max_lat": 16.0, "min_lon": 71.5, "max_lon": 73.0},
        "u_current_ms": u_current,
        "v_current_ms": v_current,
        "u_wind10_ms": u_wind10,
        "v_wind10_ms": v_wind10,
        "sea_surface_temp_c": 29.5,
        "wave_height_m": 1.2,
        "source": "SYNTHETIC_ANALYTICAL_TRUTH"
    }
    with open(os.path.join(output_dir, "metocean.json"), "w", encoding="utf-8") as f:
        json.dump(metocean_data, f, indent=2)

    # 3. True Spill Origin & Displacement Physics
    origin_lat = 15.500
    origin_lon = 72.200
    drift_duration_s = (t_sat - t_release_true).total_seconds()  # 21,600 s

    dx_meters = net_u_drift * drift_duration_s  # 8164.8 m
    dy_meters = net_v_drift * drift_duration_s  # -5313.6 m

    m_per_lat = 111320.0
    m_per_lon = 111320.0 * math.cos(math.radians(origin_lat))

    obs_centroid_lat = origin_lat + (dy_meters / m_per_lat)  # ~15.4523 deg N
    obs_centroid_lon = origin_lon + (dx_meters / m_per_lon)  # ~72.2761 deg E

    # Slick Geometry: Elongated ellipse along drift direction
    drift_angle_rad = math.atan2(net_v_drift, net_u_drift)
    major_len_km = 4.2  # diffusion + continuous discharge length
    minor_len_km = 1.1
    elongation = major_len_km / minor_len_km
    area_km2 = math.pi * (major_len_km / 2.0) * (minor_len_km / 2.0)
    perimeter_km = math.pi * (3 * (major_len_km + minor_len_km) / 2.0 - math.sqrt((3 * major_len_km / 2.0 + minor_len_km / 2.0) * (major_len_km / 2.0 + 3 * minor_len_km / 2.0)))

    # Generate ellipse polygon coordinates (lon, lat)
    num_pts = 36
    slick_ring: List[List[float]] = []
    for i in range(num_pts + 1):
        angle = 2.0 * math.pi * (i % num_pts) / num_pts
        # Ellipse in local (x, y) km
        x_loc = (major_len_km / 2.0) * math.cos(angle)
        y_loc = (minor_len_km / 2.0) * math.sin(angle)
        # Rotate by drift angle
        x_rot = x_loc * math.cos(drift_angle_rad) - y_loc * math.sin(drift_angle_rad)
        y_rot = x_loc * math.sin(drift_angle_rad) + y_loc * math.cos(drift_angle_rad)
        # Convert to degrees
        pt_lat = obs_centroid_lat + (y_rot * 1000.0 / m_per_lat)
        pt_lon = obs_centroid_lon + (x_rot * 1000.0 / m_per_lon)
        slick_ring.append([round(pt_lon, 6), round(pt_lat, 6)])

    slick_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "spill_id": "SYNTH_SPILL_001",
                    "scene_id": "SYNTH_S1A_20240510_1600",
                    "area_km2": round(area_km2, 2),
                    "perimeter_km": round(perimeter_km, 2),
                    "centroid": {"latitude": round(obs_centroid_lat, 6), "longitude": round(obs_centroid_lon, 6)},
                    "major_axis_len_km": major_len_km,
                    "minor_axis_len_km": minor_len_km,
                    "orientation_deg": round((math.degrees(drift_angle_rad) + 360) % 360, 1),
                    "elongation": round(elongation, 2),
                    "confidence": 0.94,
                    "true_origin": {"latitude": origin_lat, "longitude": origin_lon, "release_time": t_release_true.isoformat()},
                    "provenance": "SYNTHETIC_ANALYTICAL_GROUND_TRUTH"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [slick_ring]
                }
            }
        ]
    }
    with open(os.path.join(output_dir, "detected_slick.geojson"), "w", encoding="utf-8") as f:
        json.dump(slick_geojson, f, indent=2)

    # 4. AIS Vessel Trajectories
    # We construct 3 candidate vessels to stress-test the attribution & falsification engines:
    # Ship Alpha (MMSI 419000111) -> The TRUE source
    # Ship Beta  (MMSI 419000222) -> The DECOY nearby ship (spatial proximity trap, temporal conflict)
    # Ship Gamma (MMSI 419000333) -> The CONFLICTING ship (heading upstream, AIS gap)

    ais_records = []

    # Ship Alpha (MV Ocean Pioneer): transiting SSE at 12 knots (~6.17 m/s)
    # Crosses (15.500, 72.200) at exactly 10:00 UTC
    speed_alpha = 12.0
    cog_alpha = 155.0
    alpha_v_lat = -(speed_alpha * 0.514444 * 3600.0 * math.cos(math.radians(cog_alpha))) / m_per_lat
    alpha_v_lon = (speed_alpha * 0.514444 * 3600.0 * math.sin(math.radians(cog_alpha))) / m_per_lon

    for step_h in range(0, 15):
        t_pt = t_start + timedelta(hours=step_h)
        delta_h = (t_pt - t_release_true).total_seconds() / 3600.0
        p_lat = origin_lat + delta_h * alpha_v_lat
        p_lon = origin_lon + delta_h * alpha_v_lon
        ais_records.append({
            "MMSI": "419000111",
            "VesselName": "MV Ocean Pioneer",
            "VesselType": "Crude Oil Tanker",
            "Timestamp": t_pt.isoformat(),
            "Latitude": round(p_lat, 6),
            "Longitude": round(p_lon, 6),
            "SOG": speed_alpha,
            "COG": cog_alpha,
            "Heading": cog_alpha
        })

    # Ship Beta (MT Coastal Trader): Container ship at 18 knots heading East (90 deg)
    # Passes through the SLICK'S OBSERVED LOCATION at 15:30 UTC (only 30 mins before SAR pass)
    # Cannot be the source because 30 mins is insufficient to form an 8 km drifted plume!
    speed_beta = 18.0
    cog_beta = 90.0
    t_beta_cross = t_sat - timedelta(minutes=30)  # 15:30 UTC
    beta_v_lon = (speed_beta * 0.514444 * 3600.0) / m_per_lon

    for step_h in range(0, 15):
        t_pt = t_start + timedelta(hours=step_h)
        delta_h = (t_pt - t_beta_cross).total_seconds() / 3600.0
        p_lat = obs_centroid_lat + 0.005 * math.sin(step_h)
        p_lon = obs_centroid_lon + delta_h * beta_v_lon
        ais_records.append({
            "MMSI": "419000222",
            "VesselName": "MT Coastal Trader",
            "VesselType": "Container Ship",
            "Timestamp": t_pt.isoformat(),
            "Latitude": round(p_lat, 6),
            "Longitude": round(p_lon, 6),
            "SOG": speed_beta,
            "COG": cog_beta,
            "Heading": cog_beta
        })

    # Ship Gamma (MV Arabian Star): Bulk carrier at 10 knots heading NW (315 deg)
    # Moving AGAINST current; has a 3-hour transponder gap between 11:00 and 14:00 UTC
    speed_gamma = 10.0
    cog_gamma = 315.0
    gamma_lat_0 = 15.200
    gamma_lon_0 = 72.600
    gamma_v_lat = (speed_gamma * 0.514444 * 3600.0 * math.cos(math.radians(cog_gamma))) / m_per_lat
    gamma_v_lon = (speed_gamma * 0.514444 * 3600.0 * math.sin(math.radians(cog_gamma))) / m_per_lon

    for step_h in range(0, 15):
        t_pt = t_start + timedelta(hours=step_h)
        # Simulate deliberate or accidental AIS silence between 11:00 and 14:00 UTC
        if datetime(2024, 5, 10, 11, 0, 0, tzinfo=timezone.utc) <= t_pt <= datetime(2024, 5, 10, 14, 0, 0, tzinfo=timezone.utc):
            continue
        delta_h = (t_pt - t_start).total_seconds() / 3600.0
        p_lat = gamma_lat_0 + delta_h * gamma_v_lat
        p_lon = gamma_lon_0 + delta_h * gamma_v_lon
        ais_records.append({
            "MMSI": "419000333",
            "VesselName": "MV Arabian Star",
            "VesselType": "Bulk Carrier",
            "Timestamp": t_pt.isoformat(),
            "Latitude": round(p_lat, 6),
            "Longitude": round(p_lon, 6),
            "SOG": speed_gamma,
            "COG": cog_gamma,
            "Heading": cog_gamma
        })

    # Write AIS CSV
    ais_csv_path = os.path.join(output_dir, "vessel_traffic.csv")
    import csv
    with open(ais_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["MMSI", "VesselName", "VesselType", "Timestamp", "Latitude", "Longitude", "SOG", "COG", "Heading"])
        writer.writeheader()
        writer.writerows(ais_records)

    # 5. Metadata Index Record
    metadata = {
        "case_id": "CASE_005_SYNTHETIC_CHALLENGE",
        "title": "Adversarial Multi-Candidate Synthetic Forensic Benchmark",
        "t_start": t_start.isoformat(),
        "t_sat": t_sat.isoformat(),
        "ground_truth": {
            "true_polluter_mmsi": "419000111",
            "true_polluter_name": "MV Ocean Pioneer",
            "true_release_time": t_release_true.isoformat(),
            "true_release_location": {"latitude": origin_lat, "longitude": origin_lon},
            "net_drift_vector": {"u_drift_ms": net_u_drift, "v_drift_ms": net_v_drift},
            "decoy_vessel_mmsi": "419000222",
            "gap_vessel_mmsi": "419000333"
        }
    }
    with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return metadata


if __name__ == "__main__":
    meta = generate_benchmark_scenario()
    print(f"Generated synthetic benchmark scenario in data/synthetic/: {meta['case_id']}")
