import React, { useState, useEffect, useRef } from 'react';
import { 
  Shield, 
  AlertTriangle, 
  Compass, 
  Wind, 
  Waves, 
  Ship, 
  Search, 
  HelpCircle, 
  Crosshair, 
  Download, 
  BarChart3, 
  ChevronDown, 
  ChevronUp, 
  CheckCircle2, 
  XCircle, 
  RefreshCw,
  Eye,
  Sliders,
  Radio
} from 'lucide-react';

import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface Hypothesis {
  hypothesis_id: string;
  type: string;
  subject_id: string;
  subject_name: string;
  prior_probability: number;
  posterior_probability: number;
  supporting_evidence: any[];
  contradicting_evidence: any[];
  is_falsified: boolean;
  falsification?: any;
}

interface Dossier {
  incident_id: string;
  title: string;
  incident_time: string;
  location: { latitude: number; longitude: number };
  decision: string;
  leading_hypothesis_id?: string;
  leading_subject_name?: string;
  attribution_confidence: number;
  entropy_bits: number;
  is_abstention: boolean;
  abstention_reason?: string;
  hypotheses: Hypothesis[];
  origin_estimate?: any;
  detected_slick?: any;
  recommended_evidence: any[];
  audit_trail: any;
}

export default function App() {
  const [dossier, setDossier] = useState<Dossier | null>(null);
  const [loading, setLoading] = useState(true);
  const [hindcastHours, setHindcastHours] = useState(6.0);
  const [selectedHypId, setSelectedHypId] = useState<string | null>(null);
  const [expandedWhyId, setExpandedWhyId] = useState<string | null>(null);
  const [falsificationModal, setFalsificationModal] = useState<any | null>(null);
  const [comparisonData, setComparisonData] = useState<any | null>(null);
  const [showComparison, setShowComparison] = useState(false);
  
  // Layer visibility toggles
  const [showSlick, setShowSlick] = useState(true);
  const [showOrigin, setShowOrigin] = useState(true);
  const [showAIS, setShowAIS] = useState(true);

  const mapRef = useRef<any>(null);
  const mapInstance = useRef<any>(null);
  const layersGroup = useRef<any>(null);

  // 1. Fetch Investigation Dossier
  const fetchInvestigation = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/investigation/run?case_id=CASE_005_SYNTHETIC_CHALLENGE&hindcast_hours=${hindcastHours}`, {
        method: 'POST'
      });
      const data = await res.json();
      setDossier(data);
      if (data.leading_hypothesis_id) {
        setSelectedHypId(data.leading_hypothesis_id);
      }
    } catch (err) {
      console.error('Failed to run investigation:', err);
    } finally {
      setLoading(false);
    }
  };

  // 2. Fetch Comparison Data
  const fetchComparison = async () => {
    try {
      const res = await fetch('/api/v1/evaluation/compare?case_id=CASE_005_SYNTHETIC_CHALLENGE');
      const data = await res.json();
      setComparisonData(data);
      setShowComparison(true);
    } catch (err) {
      console.error('Failed to fetch comparison:', err);
    }
  };

  // 3. Attack Hypothesis Action
  const attackHypothesis = async (hypId: string) => {
    try {
      const res = await fetch(`/api/v1/falsification/attack?case_id=CASE_005_SYNTHETIC_CHALLENGE&hypothesis_id=${hypId}`, {
        method: 'POST'
      });
      const data = await res.json();
      setFalsificationModal({ hypId, result: data });
    } catch (err) {
      console.error('Attack failed:', err);
    }
  };

  useEffect(() => {
    fetchInvestigation();
  }, [hindcastHours]);

  // 4. Initialize Map
  useEffect(() => {
    if (!mapRef.current || mapInstance.current) return;

    // Center on Arabian Sea Benchmark
    const map = L.map(mapRef.current, {
      center: [15.48, 72.24],
      zoom: 11,
      zoomControl: false,
      preferCanvas: true
    });

    L.control.zoom({ position: 'topleft' }).addTo(map);

    // 100% Key-Free, Open-Access Basemaps (No API Key Required)
    const osmDark = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      className: 'dark-osm-tiles',
      maxZoom: 19
    }).addTo(map);

    const esriOcean = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Tiles &copy; Esri &mdash; GEBCO, NOAA',
      maxZoom: 13
    });

    const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Tiles &copy; Esri, Earthstar Geographics',
      maxZoom: 18
    });

    L.control.layers({
      'Dark Forensics (Key-Free)': osmDark,
      'Ocean Nautical (ESRI)': esriOcean,
      'Satellite Imagery (ESRI)': esriSatellite
    }, undefined, { position: 'bottomleft' }).addTo(map);


    layersGroup.current = L.layerGroup().addTo(map);
    mapInstance.current = map;

    // Ensure map computes its container bounding box properly
    setTimeout(() => {
      map.invalidateSize();
    }, 100);

    const handleResize = () => {
      map.invalidateSize();
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);


  // 5. Update Map Layers on Dossier Change
  useEffect(() => {
    if (!mapInstance.current || !layersGroup.current || !dossier) return;

    layersGroup.current.clearLayers();

    // Render Origin Probability Contours (Cyan / Violet)
    if (showOrigin && dossier.origin_estimate?.contour_geojson) {
      const colors = ['#8b5cf6', '#00f0ff', '#10b981'];
      let cIdx = 0;
      for (const feat of dossier.origin_estimate.contour_geojson.features) {
        const ring = feat.geometry.coordinates[0].map((pt: number[]) => [pt[1], pt[0]]);
        L.polygon(ring, {
          color: colors[cIdx % colors.length],
          weight: 1.5,
          fillColor: colors[cIdx % colors.length],
          fillOpacity: 0.12,
          dashArray: '4, 4'
        }).bindTooltip(`${feat.properties.level}`, { permanent: false }).addTo(layersGroup.current);
        cIdx++;
      }

      // Origin Centroid Marker
      const c = dossier.origin_estimate.estimated_centroid;
      L.circleMarker([c.latitude, c.longitude], {
        radius: 6,
        color: '#00f0ff',
        fillColor: '#00f0ff',
        fillOpacity: 0.9
      }).bindPopup(`<b>Reconstructed Origin Centroid</b><br>Lat: ${c.latitude.toFixed(4)}°N<br>Lon: ${c.longitude.toFixed(4)}°E`).addTo(layersGroup.current);
    }

    // Render Detected Slick Polygon (Amber Glow)
    if (showSlick && dossier.detected_slick) {
      const slickCoords = dossier.detected_slick.coordinates[0].map((pt: number[]) => [pt[1], pt[0]]);
      L.polygon(slickCoords, {
        color: '#ffb703',
        weight: 2.5,
        fillColor: '#fb8500',
        fillOpacity: 0.45
      }).bindPopup(`
        <b>Satellite Detected Slick</b><br>
        Area: ${dossier.detected_slick.area_km2} km²<br>
        Perimeter: ${dossier.detected_slick.perimeter_km} km<br>
        Elongation: ${dossier.detected_slick.elongation}<br>
        Orientation: ${dossier.detected_slick.orientation_deg}°
      `).addTo(layersGroup.current);
    }

    // Render AIS Tracks
    if (showAIS) {
      // Fetch and draw AIS lines
      fetch('/api/v1/investigation/layers/CASE_005_SYNTHETIC_CHALLENGE')
        .then(r => r.json())
        .then(geo => {
          for (const feat of geo.features) {
            if (feat.properties.layer_type === 'AIS_TRACK') {
              const coords = feat.geometry.coordinates.map((pt: number[]) => [pt[1], pt[0]]);
              const mmsi = feat.properties.mmsi;
              let trackColor = '#3b82f6';
              if (mmsi === '419000111') trackColor = '#10b981'; // Alpha
              if (mmsi === '419000222') trackColor = '#f59e0b'; // Beta
              if (mmsi === '419000333') trackColor = '#ef4444'; // Gamma

              L.polyline(coords, {
                color: trackColor,
                weight: 2,
                opacity: 0.85
              }).bindTooltip(`<b>${feat.properties.vessel_name}</b> (${feat.properties.vessel_type})`, { sticky: true }).addTo(layersGroup.current);

              // Add start and end points
              if (coords.length > 0) {
                const lastPt = coords[coords.length - 1];
                L.circleMarker(lastPt, {
                  radius: 4,
                  color: trackColor,
                  fillColor: trackColor,
                  fillOpacity: 1
                }).addTo(layersGroup.current);
              }
            }
          }
        });
    }
  }, [dossier, showSlick, showOrigin, showAIS]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', background: 'var(--bg-primary)' }}>
      {/* 1. TOP COMMAND BAR */}
      <header style={{
        height: '52px',
        background: 'var(--bg-secondary)',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 16px',
        zIndex: 1000
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            background: 'rgba(0, 240, 255, 0.1)',
            border: '1px solid var(--accent-cyan)',
            padding: '6px',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center'
          }}>
            <Shield size={20} color="var(--accent-cyan)" />
          </div>
          <div>
            <h1 style={{ fontSize: '15px', fontWeight: 800, letterSpacing: '0.05em', color: '#fff' }}>
              MARITIME FORENSICS <span style={{ color: 'var(--accent-cyan)', fontWeight: 400 }}>| SIH26143</span>
            </h1>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Operational Incident Intelligence & Oil Spill Source Attribution Workstation
            </p>
          </div>
        </div>

        {/* Status Indicators */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'rgba(16, 185, 129, 0.1)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            padding: '4px 10px',
            borderRadius: '20px',
            fontSize: '11px',
            color: 'var(--accent-emerald)'
          }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent-emerald)' }} />
            AIR-GAPPED DEMO MODE
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'rgba(59, 130, 246, 0.1)',
            border: '1px solid rgba(59, 130, 246, 0.3)',
            padding: '4px 10px',
            borderRadius: '20px',
            fontSize: '11px',
            color: 'var(--accent-blue)'
          }}>
            CASE: CASE_005_SYNTHETIC
          </div>

          <button
            onClick={fetchComparison}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'var(--bg-tertiary)',
              border: '1px solid var(--border-color)',
              color: '#fff',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600
            }}
          >
            <BarChart3 size={14} color="var(--accent-cyan)" />
            Baseline vs. Proposed
          </button>

          <button
            onClick={() => {
              if (!dossier) return;
              const blob = new Blob([JSON.stringify(dossier, null, 2)], { type: 'application/json' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `dossier_${dossier.incident_id}.json`;
              a.click();
            }}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'var(--accent-cyan)',
              border: 'none',
              color: '#000',
              padding: '6px 14px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 700
            }}
          >
            <Download size={14} />
            Export Dossier
          </button>
        </div>
      </header>

      {/* 2. MAIN 3-COLUMN WORKSTATION BODY */}
      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr 400px', flex: 1, overflow: 'hidden' }}>
        
        {/* LEFT COLUMN: ENVIRONMENTAL & OBSERVATIONAL CONTEXT */}
        <aside style={{
          background: 'var(--bg-secondary)',
          borderRight: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          padding: '16px',
          gap: '14px',
          overflowY: 'auto'
        }}>
          {/* Incident Badge */}
          <div className="glass-panel" style={{ padding: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Incident Context</span>
              <span className="mono" style={{ fontSize: '11px', color: 'var(--accent-cyan)' }}>CASE_005</span>
            </div>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#fff', marginBottom: '6px' }}>Arabian Sea Multi-Vessel Incident</h3>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
              Synthetic multi-candidate benchmark with analytical current, decoy ship, and look-alike anomaly.
            </p>
          </div>

          {/* Satellite Scene Specs */}
          <div className="glass-panel" style={{ padding: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Radio size={16} color="var(--accent-blue)" />
              <h4 style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Spaceborne SAR Observation</h4>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '12px' }}>
              <div>
                <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>SENSOR</span>
                <p className="mono" style={{ color: '#fff', fontWeight: 600 }}>Sentinel-1 C-SAR</p>
              </div>
              <div>
                <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>MODE / POL</span>
                <p className="mono" style={{ color: '#fff', fontWeight: 600 }}>IW / VV+VH</p>
              </div>
              <div>
                <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>ACQUISITION TIME</span>
                <p className="mono" style={{ color: 'var(--accent-cyan)', fontSize: '11px' }}>16:00:00 UTC</p>
              </div>
              <div>
                <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>LOOK-ALIKE RISK</span>
                <p className="mono" style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>LOW (PASS)</p>
              </div>
            </div>
          </div>

          {/* Metocean Environmental Station */}
          <div className="glass-panel" style={{ padding: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Waves size={16} color="var(--accent-cyan)" />
              <h4 style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Metocean Drift Forcing</h4>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: 'var(--text-muted)' }}>Surface Current (CMEMS)</span>
                <span className="mono" style={{ color: '#fff', fontWeight: 600 }}>0.29 m/s @ 121°</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: 'var(--text-muted)' }}>10m Wind Speed (ERA5)</span>
                <span className="mono" style={{ color: '#fff', fontWeight: 600 }}>5.00 m/s @ 127°</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '6px', borderTop: '1px solid var(--border-color)' }}>
                <span style={{ color: 'var(--accent-cyan)', fontWeight: 600 }}>Net Surface Drift</span>
                <span className="mono" style={{ color: 'var(--accent-cyan)', fontWeight: 700 }}>0.45 m/s @ 123°</span>
              </div>
            </div>
          </div>

          {/* Detected Slick Geometry */}
          {dossier?.detected_slick && (
            <div className="glass-panel" style={{ padding: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                <Compass size={16} color="var(--accent-amber)" />
                <h4 style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Slick Morphology</h4>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '12px' }}>
                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>AREA</span>
                  <p className="mono" style={{ color: 'var(--accent-amber)', fontWeight: 700 }}>{dossier.detected_slick.area_km2} km²</p>
                </div>
                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>PERIMETER</span>
                  <p className="mono" style={{ color: '#fff' }}>{dossier.detected_slick.perimeter_km} km</p>
                </div>
                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>ELONGATION</span>
                  <p className="mono" style={{ color: '#fff' }}>{dossier.detected_slick.elongation}:1</p>
                </div>
                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>ORIENTATION</span>
                  <p className="mono" style={{ color: '#fff' }}>{dossier.detected_slick.orientation_deg}°</p>
                </div>
              </div>
            </div>
          )}

          {/* Hindcast Simulation Controls */}
          <div className="glass-panel" style={{ padding: '12px', marginTop: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Hindcast Duration</span>
              <span className="mono" style={{ color: 'var(--accent-cyan)', fontWeight: 700 }}>{hindcastHours.toFixed(1)} hrs</span>
            </div>
            <input
              type="range"
              min="1.0"
              max="24.0"
              step="0.5"
              value={hindcastHours}
              onChange={(e) => setHindcastHours(parseFloat(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--accent-cyan)', marginBottom: '10px' }}
            />
            <button
              onClick={fetchInvestigation}
              disabled={loading}
              style={{
                width: '100%',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--accent-cyan)',
                color: 'var(--accent-cyan)',
                padding: '8px',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px'
              }}
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              {loading ? 'Simulating...' : 'Re-Run Hindcast & Evidence'}
            </button>
          </div>
        </aside>

        {/* CENTER COLUMN: HIGH-DENSITY GEOSPATIAL MAP */}
        <main style={{ position: 'relative', width: '100%', height: '100%', minHeight: '100%', overflow: 'hidden' }}>
          <div ref={mapRef} style={{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 }} />


          {/* Map Layer Control Widget */}
          <div style={{
            position: 'absolute',
            top: '16px',
            right: '16px',
            zIndex: 500,
            background: 'rgba(15, 22, 36, 0.88)',
            backdropFilter: 'blur(8px)',
            border: '1px solid var(--border-color)',
            borderRadius: '6px',
            padding: '10px 14px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
            fontSize: '12px'
          }}>
            <span style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }}>MAP LAYERS</span>
            
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input type="checkbox" checked={showSlick} onChange={() => setShowSlick(!showSlick)} />
              <span style={{ display: 'inline-block', width: '10px', height: '10px', background: '#ffb703', borderRadius: '2px' }} />
              Satellite Slick
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input type="checkbox" checked={showOrigin} onChange={() => setShowOrigin(!showOrigin)} />
              <span style={{ display: 'inline-block', width: '10px', height: '10px', background: '#00f0ff', borderRadius: '2px' }} />
              Origin Probability (KDE)
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input type="checkbox" checked={showAIS} onChange={() => setShowAIS(!showAIS)} />
              <span style={{ display: 'inline-block', width: '10px', height: '10px', background: '#3b82f6', borderRadius: '2px' }} />
              Historical AIS Tracks
            </label>
          </div>

          {/* Map Legend Footer */}
          <div style={{
            position: 'absolute',
            bottom: '16px',
            left: '16px',
            zIndex: 500,
            background: 'rgba(15, 22, 36, 0.88)',
            backdropFilter: 'blur(8px)',
            border: '1px solid var(--border-color)',
            borderRadius: '6px',
            padding: '8px 12px',
            display: 'flex',
            alignItems: 'center',
            gap: '16px',
            fontSize: '11px',
            color: 'var(--text-muted)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981' }} />
              Alpha (MV Ocean Pioneer)
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#f59e0b' }} />
              Beta (MT Coastal Trader)
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#ef4444' }} />
              Gamma (MV Arabian Star)
            </div>
          </div>
        </main>

        {/* RIGHT COLUMN: FORENSIC ATTRIBUTION & ACTIVE SENSING */}
        <aside style={{
          background: 'var(--bg-secondary)',
          borderLeft: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          padding: '16px',
          gap: '14px',
          overflowY: 'auto'
        }}>
          {/* Top Attribution Decision Banner */}
          {dossier && (
            <div className={`glass-panel ${dossier.is_abstention ? 'glow-amber' : 'glow-emerald'}`} style={{
              padding: '14px',
              borderLeft: `4px solid ${dossier.is_abstention ? 'var(--accent-amber)' : 'var(--accent-emerald)'}`
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <span style={{ fontSize: '10px', letterSpacing: '0.05em', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Attribution Decision</span>
                <span className="mono" style={{ fontSize: '11px', color: dossier.is_abstention ? 'var(--accent-amber)' : 'var(--accent-emerald)', fontWeight: 700 }}>
                  {dossier.decision.toUpperCase()}
                </span>
              </div>

              {!dossier.is_abstention ? (
                <div>
                  <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#fff', marginBottom: '4px' }}>
                    {dossier.leading_subject_name}
                  </h2>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Calibrated Confidence:</span>
                    <span className="mono" style={{ color: 'var(--accent-emerald)', fontWeight: 700 }}>
                      {(dossier.attribution_confidence * 100).toFixed(1)}%
                    </span>
                    <span style={{ color: 'var(--text-dim)' }}>|</span>
                    <span style={{ color: 'var(--text-muted)' }}>Entropy:</span>
                    <span className="mono" style={{ color: '#fff' }}>{dossier.entropy_bits.toFixed(2)} bits</span>
                  </div>
                </div>
              ) : (
                <div>
                  <h3 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--accent-amber)', marginBottom: '4px' }}>
                    Abstention: Insufficient Evidence
                  </h3>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                    {dossier.abstention_reason}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Multi-Hypothesis Ranking Station */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <h4 style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
                Competing Hypotheses ({dossier?.hypotheses?.length || 0})
              </h4>
              <span style={{ fontSize: '10px', color: 'var(--text-dim)' }}>Bayesian Posterior P(H|E)</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {dossier?.hypotheses?.map((hyp) => {
                const isSelected = selectedHypId === hyp.hypothesis_id;
                const isWhyOpen = expandedWhyId === hyp.hypothesis_id;

                return (
                  <div 
                    key={hyp.hypothesis_id}
                    className="glass-panel"
                    style={{
                      padding: '10px 12px',
                      border: isSelected ? '1px solid var(--accent-cyan)' : '1px solid var(--border-color)',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '6px' }}>
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span style={{ fontSize: '13px', fontWeight: 700, color: '#fff' }}>{hyp.subject_name}</span>
                          {hyp.is_falsified && (
                            <span style={{
                              fontSize: '9px',
                              background: 'rgba(239, 68, 68, 0.15)',
                              color: 'var(--accent-rose)',
                              padding: '1px 6px',
                              borderRadius: '4px',
                              border: '1px solid rgba(239, 68, 68, 0.4)',
                              fontWeight: 700
                            }}>
                              FALSIFIED
                            </span>
                          )}
                        </div>
                        <span style={{ fontSize: '10px', color: 'var(--text-dim)' }}>{hyp.type.toUpperCase()} | ID: {hyp.subject_id}</span>
                      </div>

                      <div style={{ textAlign: 'right' }}>
                        <span className="mono" style={{ fontSize: '14px', fontWeight: 800, color: hyp.is_falsified ? 'var(--text-dim)' : 'var(--accent-cyan)' }}>
                          {(hyp.posterior_probability * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    {/* Posterior Bar */}
                    <div style={{ width: '100%', height: '4px', background: 'var(--bg-tertiary)', borderRadius: '2px', overflow: 'hidden', marginBottom: '8px' }}>
                      <div style={{
                        width: `${Math.min(100, Math.max(1, hyp.posterior_probability * 100))}%`,
                        height: '100%',
                        background: hyp.is_falsified ? 'var(--accent-rose)' : 'var(--accent-cyan)'
                      }} />
                    </div>

                    {/* Interactive Action Buttons */}
                    <div style={{ display: 'flex', gap: '8px' }}>
                      {/* WHY BUTTON */}
                      <button
                        onClick={() => setExpandedWhyId(isWhyOpen ? null : hyp.hypothesis_id)}
                        style={{
                          flex: 1,
                          background: 'rgba(255, 255, 255, 0.04)',
                          border: '1px solid var(--border-color)',
                          color: 'var(--text-muted)',
                          padding: '5px',
                          borderRadius: '4px',
                          fontSize: '11px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '4px'
                        }}
                      >
                        <HelpCircle size={12} color="var(--accent-cyan)" />
                        WHY?
                        {isWhyOpen ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                      </button>

                      {/* ATTACK HYPOTHESIS BUTTON */}
                      <button
                        onClick={() => attackHypothesis(hyp.hypothesis_id)}
                        style={{
                          flex: 1,
                          background: 'rgba(239, 68, 68, 0.08)',
                          border: '1px solid rgba(239, 68, 68, 0.35)',
                          color: 'var(--accent-rose)',
                          padding: '5px',
                          borderRadius: '4px',
                          fontSize: '11px',
                          fontWeight: 700,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '4px'
                        }}
                      >
                        <Crosshair size={12} />
                        ATTACK
                      </button>
                    </div>

                    {/* EXPANDED "WHY?" EVIDENCE DRAWER */}
                    {isWhyOpen && (
                      <div style={{
                        marginTop: '10px',
                        padding: '10px',
                        background: 'rgba(0, 0, 0, 0.3)',
                        borderRadius: '6px',
                        border: '1px solid var(--border-color)',
                        fontSize: '11px'
                      }}>
                        <div style={{ marginBottom: '8px' }}>
                          <span style={{ color: 'var(--accent-emerald)', fontWeight: 700 }}>Supporting Evidence [+]</span>
                          {hyp.supporting_evidence.length === 0 ? (
                            <p style={{ color: 'var(--text-dim)', fontStyle: 'italic' }}>None recorded</p>
                          ) : (
                            hyp.supporting_evidence.map((ev, i) => (
                              <div key={i} style={{ display: 'flex', gap: '6px', marginTop: '4px', color: 'var(--text-muted)' }}>
                                <CheckCircle2 size={12} color="var(--accent-emerald)" style={{ flexShrink: 0, marginTop: '2px' }} />
                                <span>{ev.explanation}</span>
                              </div>
                            ))
                          )}
                        </div>

                        <div>
                          <span style={{ color: 'var(--accent-rose)', fontWeight: 700 }}>Contradicting Evidence [-]</span>
                          {hyp.contradicting_evidence.length === 0 ? (
                            <p style={{ color: 'var(--text-dim)', fontStyle: 'italic' }}>None recorded</p>
                          ) : (
                            hyp.contradicting_evidence.map((ev, i) => (
                              <div key={i} style={{ display: 'flex', gap: '6px', marginTop: '4px', color: 'var(--text-muted)' }}>
                                <XCircle size={12} color="var(--accent-rose)" style={{ flexShrink: 0, marginTop: '2px' }} />
                                <span>{ev.explanation}</span>
                              </div>
                            ))
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* SIGNATURE "WHAT SHOULD WE CHECK NEXT?" ACTIVE SENSING PANEL */}
          <div className="glass-panel glow-cyan" style={{ padding: '14px', border: '1px solid rgba(0, 240, 255, 0.3)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <Eye size={16} color="var(--accent-cyan)" />
              <h4 style={{ fontSize: '13px', fontWeight: 800, color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Next-Best-Evidence Recommendations
              </h4>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Information-theoretic sensor tasking ranked by Expected Entropy Reduction E[ΔH]:
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {dossier?.recommended_evidence?.map((rec, idx) => (
                <div 
                  key={idx}
                  style={{
                    background: 'rgba(0, 0, 0, 0.4)',
                    border: '1px solid var(--border-color)',
                    padding: '8px 10px',
                    borderRadius: '6px'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: '#fff' }}>{rec.action_type}</span>
                    <span className="mono" style={{
                      fontSize: '10px',
                      background: 'rgba(0, 240, 255, 0.1)',
                      color: 'var(--accent-cyan)',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      border: '1px solid rgba(0, 240, 255, 0.25)'
                    }}>
                      +{rec.expected_information_gain_bits} bits E[ΔH]
                    </span>
                  </div>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)', lineHeight: '1.35' }}>
                    {rec.rationale}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </div>

      {/* 3. FALSIFICATION ATTACK RESULT MODAL */}
      {falsificationModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0, 0, 0, 0.75)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 2000
        }}>
          <div className="glass-panel" style={{ width: '520px', padding: '20px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Crosshair size={20} color="var(--accent-rose)" />
                <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#fff' }}>Adversarial Falsification Attack</h3>
              </div>
              <button 
                onClick={() => setFalsificationModal(null)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', fontSize: '18px' }}
              >
                ✕
              </button>
            </div>

            <div style={{
              padding: '12px',
              borderRadius: '6px',
              background: falsificationModal.result.survives ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
              border: `1px solid ${falsificationModal.result.survives ? 'var(--accent-emerald)' : 'var(--accent-rose)'}`,
              marginBottom: '14px'
            }}>
              <p style={{
                fontSize: '14px',
                fontWeight: 800,
                color: falsificationModal.result.survives ? 'var(--accent-emerald)' : 'var(--accent-rose)'
              }}>
                {falsificationModal.result.survives ? '✓ HYPOTHESIS SURVIVES ATTACK' : '✕ HYPOTHESIS FALSIFIED & DISPROVEN'}
              </p>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                Passed {falsificationModal.result.challenges_passed} of 5 challenges. Failed {falsificationModal.result.challenges_failed}.
              </p>
            </div>

            {/* Contradiction details */}
            {falsificationModal.result.contradicting_reasons?.length > 0 && (
              <div style={{ marginBottom: '14px' }}>
                <h5 style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '6px' }}>Identified Contradictions</h5>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {falsificationModal.result.contradicting_reasons.map((r: string, idx: number) => (
                    <div key={idx} style={{ display: 'flex', gap: '6px', fontSize: '12px', color: 'var(--accent-rose)' }}>
                      <XCircle size={14} style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span>{r}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => setFalsificationModal(null)}
              style={{
                width: '100%',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                color: '#fff',
                padding: '8px',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: 700
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* 4. BASELINE VS PROPOSED COMPARISON MODAL */}
      {showComparison && comparisonData && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0, 0, 0, 0.75)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 2000
        }}>
          <div className="glass-panel" style={{ width: '640px', padding: '24px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <BarChart3 size={20} color="var(--accent-cyan)" />
                <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#fff' }}>Baseline vs. Proposed Forensic Engine</h3>
              </div>
              <button 
                onClick={() => setShowComparison(false)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', fontSize: '18px' }}
              >
                ✕
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '16px' }}>
              {/* Baseline Card */}
              <div className="glass-panel" style={{ padding: '14px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <h4 style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '8px' }}>HEURISTIC BASELINE</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '12px' }}>
                  <div>
                    <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>RANK 1 CANDIDATE</span>
                    <p style={{ fontWeight: 700, color: '#fff' }}>{comparisonData.baseline.top_candidate}</p>
                    <p className="mono" style={{ color: 'var(--text-muted)' }}>Score: {comparisonData.baseline.top_score}</p>
                  </div>
                  <div>
                    <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>RANK 2 CANDIDATE</span>
                    <p style={{ fontWeight: 600, color: 'var(--accent-rose)' }}>{comparisonData.baseline.rank2_candidate}</p>
                    <p className="mono" style={{ color: 'var(--text-muted)' }}>Score: {comparisonData.baseline.rank2_score}</p>
                  </div>
                  <div style={{ paddingTop: '6px', borderTop: '1px solid var(--border-color)' }}>
                    <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>SEPARATION MARGIN</span>
                    <p className="mono" style={{ color: 'var(--accent-amber)', fontWeight: 700 }}>+{comparisonData.baseline.margin_separation}</p>
                  </div>
                </div>
              </div>

              {/* Proposed Engine Card */}
              <div className="glass-panel glow-cyan" style={{ padding: '14px', border: '1px solid var(--accent-cyan)' }}>
                <h4 style={{ fontSize: '12px', fontWeight: 800, color: 'var(--accent-cyan)', marginBottom: '8px' }}>PROPOSED FORENSIC ENGINE</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '12px' }}>
                  <div>
                    <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>RANK 1 CANDIDATE</span>
                    <p style={{ fontWeight: 700, color: '#fff' }}>{comparisonData.proposed_engine.top_hypothesis}</p>
                    <p className="mono" style={{ color: 'var(--accent-emerald)', fontWeight: 700 }}>Posterior: {(comparisonData.proposed_engine.top_posterior * 100).toFixed(1)}%</p>
                  </div>
                  <div>
                    <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>RANK 2 CANDIDATE</span>
                    <p style={{ fontWeight: 600, color: 'var(--text-muted)' }}>{comparisonData.proposed_engine.rank2_hypothesis}</p>
                    <p className="mono" style={{ color: 'var(--text-muted)' }}>Posterior: {(comparisonData.proposed_engine.rank2_posterior * 100).toFixed(1)}%</p>
                  </div>
                  <div style={{ paddingTop: '6px', borderTop: '1px solid var(--border-color)' }}>
                    <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>SEPARATION MARGIN</span>
                    <p className="mono" style={{ color: 'var(--accent-emerald)', fontWeight: 800 }}>+{comparisonData.proposed_engine.margin_separation}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Improvement highlight banner */}
            <div style={{
              background: 'rgba(0, 240, 255, 0.08)',
              border: '1px solid rgba(0, 240, 255, 0.25)',
              padding: '12px',
              borderRadius: '6px',
              fontSize: '12px',
              marginBottom: '16px'
            }}>
              <span style={{ fontWeight: 800, color: 'var(--accent-cyan)' }}>
                +{comparisonData.improvements.candidate_separation_margin_expansion_pct}% Margin Expansion
              </span>
              <p style={{ color: 'var(--text-muted)', marginTop: '4px' }}>
                Both decoy vessels (MT Coastal Trader & MV Arabian Star) successfully falsified via hydrodynamic heading and counterfactual plume testing.
              </p>
            </div>

            <button
              onClick={() => setShowComparison(false)}
              style={{
                width: '100%',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                color: '#fff',
                padding: '8px',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: 700
              }}
            >
              Close Comparison
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
