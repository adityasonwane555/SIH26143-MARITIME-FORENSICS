"""
Sets up comprehensive, realistic case scenario files for:
- CASE_001_WAKASHIO (Mauritius Grounding)
- CASE_002_NEW_DIAMOND (Sri Lanka Tanker Fire)
- CASE_005_SYNTHETIC_CHALLENGE (Arabian Sea Benchmark)
Each with detected_slick.geojson, metocean.json, and vessel_traffic.csv.
"""

import os
import json
import csv
import shutil
import math
from datetime import datetime, timedelta, timezone

def generate_ellipse_polygon(c_lat, c_lon, major_km, minor_km, angle_deg, num_points=32):
    coords = []
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    for i in range(num_points):
        theta = 2.0 * math.pi * i / num_points
        dx_local = (major_km / 2.0) * math.cos(theta)
        dy_local = (minor_km / 2.0) * math.sin(theta)
        
        dx_km = dx_local * cos_a - dy_local * sin_a
        dy_km = dx_local * sin_a + dy_local * cos_a
        
        lat = c_lat + (dy_km / 111.0)
        lon = c_lon + (dx_km / (111.0 * math.cos(math.radians(c_lat))))
        coords.append([round(lon, 6), round(lat, 6)])
    
    coords.append(coords[0]) # close ring
    return coords


def setup_case_001_wakashio():
    case_dir = "data/cases/CASE_001_WAKASHIO"
    os.makedirs(case_dir, exist_ok=True)
    
    # 1. Metocean
    metocean = {
        "timestamp": "2020-08-06T12:00:00Z",
        "current_u_mps": -0.18,
        "current_v_mps": 0.24,
        "wind_u_mps": -6.2,
        "wind_v_mps": 4.1,
        "source": "CMEMS Global Reanalysis / ERA5",
        "sea_surface_temp_c": 24.5,
        "wave_height_m": 2.8
    }
    with open(f"{case_dir}/metocean.json", "w") as f:
        json.dump(metocean, f, indent=2)
        
    # 2. Detected Slick (Reef grounding slick off Pointe d'Esny)
    # Centroid slightly drifted northwest from reef (-20.439, 57.745)
    c_lat, c_lon = -20.428, 57.735
    coords = generate_ellipse_polygon(c_lat, c_lon, major_km=4.8, minor_km=1.4, angle_deg=315.0)
    
    slick_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "spill_id": "WAKASHIO_SLICK_001",
                    "scene_id": "S1A_IW_GRDH_20200806T144512",
                    "area_km2": 5.28,
                    "perimeter_km": 11.4,
                    "centroid_lat": c_lat,
                    "centroid_lon": c_lon,
                    "major_axis_len_km": 4.8,
                    "minor_axis_len_km": 1.4,
                    "orientation_deg": 315.0,
                    "elongation": 3.43,
                    "confidence": 0.98,
                    "quality_flag": "HIGH"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                }
            }
        ]
    }
    with open(f"{case_dir}/detected_slick.geojson", "w") as f:
        json.dump(slick_geojson, f, indent=2)
        
    # 3. AIS Vessel Traffic
    # MV Wakashio (372711000) grounded on reef, plus background patrol vessel
    t0 = datetime(2020, 8, 6, 4, 0, tzinfo=timezone.utc)
    rows = []
    
    # Track 1: MV Wakashio (Grounded stationary on reef -20.439, 57.745)
    for step in range(25):
        t = t0 + timedelta(minutes=step * 30)
        # Small GPS jitter around grounded point
        jitter = (step % 3 - 1) * 0.0001
        rows.append({
            "mmsi": "372711000",
            "vessel_name": "MV Wakashio",
            "vessel_type": "Bulk Carrier",
            "timestamp": t.isoformat(),
            "latitude": round(-20.439 + jitter, 5),
            "longitude": round(57.745 + jitter, 5),
            "sog_knots": 0.1,
            "cog_degrees": 238.0
        })
        
    # Track 2: Coast Guard Patrol CGS Barracuda (Decoy passing south 6 hours later)
    for step in range(25):
        t = t0 + timedelta(minutes=step * 30)
        lat = -20.520 + (step * 0.003)
        lon = 57.650 + (step * 0.008)
        rows.append({
            "mmsi": "645000001",
            "vessel_name": "CGS Barracuda",
            "vessel_type": "Patrol Vessel",
            "timestamp": t.isoformat(),
            "latitude": round(lat, 5),
            "longitude": round(lon, 5),
            "sog_knots": 14.5,
            "cog_degrees": 65.0
        })

    with open(f"{case_dir}/vessel_traffic.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mmsi", "vessel_name", "vessel_type", "timestamp", "latitude", "longitude", "sog_knots", "cog_degrees"])
        writer.writeheader()
        writer.writerows(rows)
        
    print("Setup CASE_001_WAKASHIO complete.")


def setup_case_002_new_diamond():
    case_dir = "data/cases/CASE_002_NEW_DIAMOND"
    os.makedirs(case_dir, exist_ok=True)
    
    # 1. Metocean
    metocean = {
        "timestamp": "2020-09-04T12:00:00Z",
        "current_u_mps": 0.38,
        "current_v_mps": 0.14,
        "wind_u_mps": 4.5,
        "wind_v_mps": 1.8,
        "source": "Copernicus CMEMS / ERA5 Southwest Monsoon",
        "sea_surface_temp_c": 29.1,
        "wave_height_m": 1.9
    }
    with open(f"{case_dir}/metocean.json", "w") as f:
        json.dump(metocean, f, indent=2)
        
    # 2. Detected Slick (Bunker slick drifting eastward from tanker)
    c_lat, c_lon = 7.125, 82.420
    coords = generate_ellipse_polygon(c_lat, c_lon, major_km=5.6, minor_km=1.8, angle_deg=75.0)
    
    slick_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "spill_id": "NEW_DIAMOND_SLICK_001",
                    "scene_id": "S1B_IW_GRDH_20200904T121545",
                    "area_km2": 7.92,
                    "perimeter_km": 14.2,
                    "centroid_lat": c_lat,
                    "centroid_lon": c_lon,
                    "major_axis_len_km": 5.6,
                    "minor_axis_len_km": 1.8,
                    "orientation_deg": 75.0,
                    "elongation": 3.11,
                    "confidence": 0.95,
                    "quality_flag": "HIGH"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                }
            }
        ]
    }
    with open(f"{case_dir}/detected_slick.geojson", "w") as f:
        json.dump(slick_geojson, f, indent=2)
        
    # 3. AIS Vessel Traffic
    # MT New Diamond (356354000) adrift at 1.2 knots with southwest monsoon current
    # Tug Rawana (417000101) attending
    # Passing Container Ship (563000888)
    t0 = datetime(2020, 9, 4, 4, 0, tzinfo=timezone.utc)
    rows = []
    
    for step in range(25):
        t = t0 + timedelta(minutes=step * 30)
        
        # New Diamond: Drifting with current eastward
        drift_lat = 7.080 + (step * 0.002)
        drift_lon = 82.320 + (step * 0.005)
        rows.append({
            "mmsi": "356354000",
            "vessel_name": "MT New Diamond",
            "vessel_type": "Crude Tanker",
            "timestamp": t.isoformat(),
            "latitude": round(drift_lat, 5),
            "longitude": round(drift_lon, 5),
            "sog_knots": 1.2,
            "cog_degrees": 75.0
        })
        
        # Tug Rawana (circling tanker in close proximity)
        angle = step * 0.4
        tug_lat = drift_lat + 0.008 * math.cos(angle)
        tug_lon = drift_lon + 0.008 * math.sin(angle)
        rows.append({
            "mmsi": "417000101",
            "vessel_name": "Tug Rawana",
            "vessel_type": "Tug / Salvage",
            "timestamp": t.isoformat(),
            "latitude": round(tug_lat, 5),
            "longitude": round(tug_lon, 5),
            "sog_knots": 4.2,
            "cog_degrees": round((math.degrees(angle) + 90) % 360, 1)
        })
        
        # Passing Container Ship 18 nm North
        c_lat_p = 7.380
        c_lon_p = 82.100 + (step * 0.015)
        rows.append({
            "mmsi": "563000888",
            "vessel_name": "MSC Teresa",
            "vessel_type": "Container Ship",
            "timestamp": t.isoformat(),
            "latitude": round(c_lat_p, 5),
            "longitude": round(c_lon_p, 5),
            "sog_knots": 18.5,
            "cog_degrees": 92.0
        })

    with open(f"{case_dir}/vessel_traffic.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mmsi", "vessel_name", "vessel_type", "timestamp", "latitude", "longitude", "sog_knots", "cog_degrees"])
        writer.writeheader()
        writer.writerows(rows)
        
    print("Setup CASE_002_NEW_DIAMOND complete.")


def setup_case_005_synthetic():
    case_dir = "data/cases/CASE_005_SYNTHETIC_CHALLENGE"
    os.makedirs(case_dir, exist_ok=True)
    shutil.copy("data/synthetic/metocean.json", f"{case_dir}/metocean.json")
    shutil.copy("data/synthetic/detected_slick.geojson", f"{case_dir}/detected_slick.geojson")
    shutil.copy("data/synthetic/vessel_traffic.csv", f"{case_dir}/vessel_traffic.csv")
    print("Setup CASE_005_SYNTHETIC_CHALLENGE complete.")


def setup_case_003_huntington():
    case_dir = "data/cases/CASE_003_HUNTINGTON"
    os.makedirs(case_dir, exist_ok=True)

    metocean = {
        "timestamp": "2021-10-02T12:00:00Z",
        "current_u_mps": 0.08,
        "current_v_mps": -0.15,
        "wind_u_mps": 2.2,
        "wind_v_mps": -3.5,
        "source": "NOAA CO-OPS / CDIP Coastal Model",
        "sea_surface_temp_c": 18.2,
        "wave_height_m": 1.1
    }
    with open(f"{case_dir}/metocean.json", "w") as f:
        json.dump(metocean, f, indent=2)

    c_lat, c_lon = 33.615, -118.045
    coords = generate_ellipse_polygon(c_lat, c_lon, major_km=5.2, minor_km=1.2, angle_deg=135.0)
    slick_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                },
                "properties": {
                    "spill_id": "HUNTINGTON_PIPELINE_SLICK_001",
                    "scene_id": "S1A_IW_GRDH_20211002T135022",
                    "acquisition_time": "2021-10-02T13:50:22Z",
                    "confidence": 0.96,
                    "sensor": "Sentinel-1 SAR C-Band"
                }
            }
        ]
    }
    with open(f"{case_dir}/detected_slick.geojson", "w") as f:
        json.dump(slick_geojson, f, indent=2)

    rows = []
    base_t = datetime(2021, 10, 2, 6, 0, 0, tzinfo=timezone.utc)
    for step in range(25):
        t = base_t + timedelta(minutes=step * 20)
        # MSC Danit (drift / slow dragging anchor in San Pedro Bay)
        d_lat = 33.630 + (step * 0.0008)
        d_lon = -118.060 + (step * 0.0005)
        rows.append({
            "mmsi": "357388000",
            "vessel_name": "MSC Danit",
            "vessel_type": "Container Ship",
            "timestamp": t.isoformat(),
            "latitude": round(d_lat, 5),
            "longitude": round(d_lon, 5),
            "sog_knots": 1.1,
            "cog_degrees": 120.0
        })
        # Beijing (anchored nearby)
        rows.append({
            "mmsi": "352898000",
            "vessel_name": "Beijing",
            "vessel_type": "Container Ship",
            "timestamp": t.isoformat(),
            "latitude": round(33.645 + math.sin(step * 0.1) * 0.001, 5),
            "longitude": round(-118.075 + math.cos(step * 0.1) * 0.001, 5),
            "sog_knots": 0.2,
            "cog_degrees": 45.0
        })
        # USCG Cutter Halibut (patrolling)
        h_lat = 33.610 + (step * 0.004)
        h_lon = -118.030 - (step * 0.003)
        rows.append({
            "mmsi": "369854000",
            "vessel_name": "USCG Cutter Halibut",
            "vessel_type": "Law Enforcement Patrol",
            "timestamp": t.isoformat(),
            "latitude": round(h_lat, 5),
            "longitude": round(h_lon, 5),
            "sog_knots": 12.0,
            "cog_degrees": 315.0
        })

    with open(f"{case_dir}/vessel_traffic.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mmsi", "vessel_name", "vessel_type", "timestamp", "latitude", "longitude", "sog_knots", "cog_degrees"])
        writer.writeheader()
        writer.writerows(rows)
    print("Setup CASE_003_HUNTINGTON complete.")


def setup_case_004_ennore():
    case_dir = "data/cases/CASE_004_ENNORE"
    os.makedirs(case_dir, exist_ok=True)

    metocean = {
        "timestamp": "2017-01-28T06:00:00Z",
        "current_u_mps": 0.15,
        "current_v_mps": 0.22,
        "wind_u_mps": -3.8,
        "wind_v_mps": -2.9,
        "source": "INCOIS Coastal Ocean Forecast",
        "sea_surface_temp_c": 27.8,
        "wave_height_m": 1.4
    }
    with open(f"{case_dir}/metocean.json", "w") as f:
        json.dump(metocean, f, indent=2)

    c_lat, c_lon = 13.265, 80.355
    coords = generate_ellipse_polygon(c_lat, c_lon, major_km=4.5, minor_km=1.1, angle_deg=25.0)
    slick_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                },
                "properties": {
                    "spill_id": "ENNORE_COLLISION_SLICK_001",
                    "scene_id": "S1A_IW_GRDH_20170128T061530",
                    "acquisition_time": "2017-01-28T06:15:30Z",
                    "confidence": 0.97,
                    "sensor": "Sentinel-1 SAR C-Band"
                }
            }
        ]
    }
    with open(f"{case_dir}/detected_slick.geojson", "w") as f:
        json.dump(slick_geojson, f, indent=2)

    rows = []
    base_t = datetime(2017, 1, 28, 0, 0, 0, tzinfo=timezone.utc)
    for step in range(25):
        t = base_t + timedelta(minutes=step * 20)
        # Dawn Kanchipuram (breached tanker, drifting slowly north)
        dk_lat = 13.250 + (step * 0.0006)
        dk_lon = 80.345 + (step * 0.0004)
        rows.append({
            "mmsi": "419071000",
            "vessel_name": "Dawn Kanchipuram",
            "vessel_type": "Product Tanker",
            "timestamp": t.isoformat(),
            "latitude": round(dk_lat, 5),
            "longitude": round(dk_lon, 5),
            "sog_knots": 0.8,
            "cog_degrees": 35.0
        })
        # BW Maple (collision partner, proceeding out)
        bm_lat = 13.255 + (step * 0.002)
        bm_lon = 80.350 + (step * 0.005)
        rows.append({
            "mmsi": "232004000",
            "vessel_name": "BW Maple",
            "vessel_type": "LPG Carrier",
            "timestamp": t.isoformat(),
            "latitude": round(bm_lat, 5),
            "longitude": round(bm_lon, 5),
            "sog_knots": 8.5,
            "cog_degrees": 70.0
        })
        # Ocean Pride (salvage tug)
        rows.append({
            "mmsi": "419000123",
            "vessel_name": "Ocean Pride",
            "vessel_type": "Port Tug",
            "timestamp": t.isoformat(),
            "latitude": round(13.245 + (step * 0.0005), 5),
            "longitude": round(80.340 + (step * 0.0003), 5),
            "sog_knots": 3.0,
            "cog_degrees": 40.0
        })

    with open(f"{case_dir}/vessel_traffic.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mmsi", "vessel_name", "vessel_type", "timestamp", "latitude", "longitude", "sog_knots", "cog_degrees"])
        writer.writeheader()
        writer.writerows(rows)
    print("Setup CASE_004_ENNORE complete.")


if __name__ == "__main__":
    setup_case_001_wakashio()
    setup_case_002_new_diamond()
    setup_case_003_huntington()
    setup_case_004_ennore()
    setup_case_005_synthetic()
    print("All incident cases initialized in data/cases/.")
