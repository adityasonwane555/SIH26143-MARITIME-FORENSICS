# Executive Limitations & Operational Boundaries Summary — SIH26143

## 1. Physical & Oceanographic Boundaries
1. **Simplified 2D Surface Advection:**
   - The current advection engine models surface slick transport using Runge-Kutta 4th-Order with 3.2% wind drag and 20° Coriolis deflection.
   - It does not currently compute full 3D vertical turbulent entrainment, droplet breakup (Stokes regime), or subsurface emulsion dissolution.
2. **Weathering Processes:**
   - Evaporation, emulsification, and photo-oxidation are represented through decay and look-alike heuristics rather than a full chemistry-specific oil weathering model (e.g. ADIOS-3).
3. **Metocean Resolution Dependency:**
   - The accuracy of reverse origin localization is bounded by the spatial ($0.083^\circ$) and temporal ($1\text{ to }3\text{ hours}$) resolution of external ocean reanalysis data (CMEMS/ERA5). Sub-mesoscale coastal eddies smaller than $9\text{ km}$ may introduce origin errors up to $1\text{ to }2\text{ km}$.

## 2. Remote Sensing & AIS Constraints
1. **Cloud & Lighting Constraints:**
   - Sentinel-1 SAR operates all-weather/day-night, but high-resolution optical tasking (Sentinel-2, PlanetScope) requires daylight and cloud-free conditions.
2. **Deliberate Dark Vessels (Spoofing & Stealth):**
   - If a polluter deliberately disables its Class-A AIS transponder and deviates from linear dead-reckoning trajectories, the system correctly attributes probability to the `DARK_VESSEL` hypothesis and recommends radar sweep tasking, but cannot independently ascertain vessel identity without optical or RF correlation.
3. **Legal Status:**
   - The system is an investigative support platform providing probabilistic attribution and falsification proofs; it does not replace formal legal judicial processes.
