# Maritime Forensics & Oil Spill Attribution: Master Reference Catalog

**Project:** SIH26143 Maritime Forensic Intelligence Engine  
**Document:** `Ref.md`  
**Classification:** Research, Data, and Technical References  
**Last Updated:** September 2026  

---

## Table of Contents

1. [Peer-Reviewed Scientific Literature](#1-peer-reviewed-scientific-literature)
   - [1.1 Lagrangian Ocean Drift & Hydrodynamic Transport](#11-lagrangian-ocean-drift--hydrodynamic-transport)
   - [1.2 Synthetic Aperture Radar (SAR) Remote Sensing & Slick Physics](#12-synthetic-aperture-radar-sar-remote-sensing--slick-physics)
   - [1.3 Bayesian Reasoning, Forensic Evidence & Adversarial Falsification](#13-bayesian-reasoning-forensic-evidence--adversarial-falsification)
   - [1.4 Information Theory, Uncertainty Quantification & Active Sensing](#14-information-theory-uncertainty-quantification--active-sensing)
2. [Operational Systems & Prior Art Benchmarks](#2-operational-systems--prior-art-benchmarks)
3. [Satellite Remote Sensing Portals & APIs](#3-satellite-remote-sensing-portals--apis)
4. [Oceanographic & Atmospheric Reanalysis Services](#4-oceanographic--atmospheric-reanalysis-services)
5. [Vessel Tracking & AIS Registries](#5-vessel-tracking--ais-registries)
6. [Benchmark Incident Ground Truth & Formal Investigation Reports](#6-benchmark-incident-ground-truth--formal-investigation-reports)
7. [International Standards, Treaties & Technical Specifications](#7-international-standards-treaties--technical-specifications)

---

## 1. Peer-Reviewed Scientific Literature

### 1.1 Lagrangian Ocean Drift & Hydrodynamic Transport

* **Dagestad, K.-F., Röhrs, J., Breivik, Ø., & Ådlandsvik, B. (2018).**  
  *OpenDrift v1.0: a flexible open source framework for ocean trajectory modelling.*  
  *Geoscientific Model Development*, 11(4), 1405–1424.  
  DOI: [10.5194/gmd-11-1405-2018](https://doi.org/10.5194/gmd-11-1405-2018)  
  *Relevance:* Primary reference for vectorized Lagrangian trajectory integration, leeway windage factors, and reversible advection mathematics.

* **ASCE Task Committee on Modeling of Oil Spills (1996).**  
  *State-of-the-art review of modeling transport and fate of oil spills.*  
  *Journal of Hydraulic Engineering*, 122(11), 594–609.  
  DOI: [10.1061/(ASCE)0733-9429(1996)122:11(594)](https://doi.org/10.1061/(ASCE)0733-9429(1996)122:11(594))  
  *Relevance:* Foundational benchmark establishing the empirical 3.0%–3.5% wind drift coefficient ($\alpha_{\text{wind}}$) and Coriolis deflection angle for oceanic oil slick transport.

* **Reed, M., Johansen, Ø., Brandvik, P. J., Daling, P., Lewis, A., Fiocco, R., Mackay, D., & Prentki, R. (1999).**  
  *Oil spill modeling towards the close of the twentieth century: Overview of the state of the art.*  
  *Spill Science & Technology Bulletin*, 5(1), 3–16.  
  DOI: [10.1016/S1353-2561(98)00029-2](https://doi.org/10.1016/S1353-2561(98)00029-2)  
  *Relevance:* Mechanical spreading, natural dispersion, Mackay evaporation kinetics, and turbulent eddy diffusivity bounds ($K_h$).

* **Al-Rabeh, A. H. (1994).**  
  *Estimating surface oil spill drift using a numerical model.*  
  *Ocean Engineering*, 21(1), 85–94.  
  DOI: [10.1016/0029-8018(94)90016-7](https://doi.org/10.1016/0029-8018(94)90016-7)  
  *Relevance:* Velocity superposition principles combining baroclinic current vectors, atmospheric wind drag, and turbulent random walks.

* **Röhrs, J., Dagestad, K.-F., & Sutherland, G. (2021).**  
  *Observation-guided Lagrangian drift forecasting with OpenDrift.*  
  *Ocean Science*, 17(5), 1361–1376.  
  DOI: [10.5194/os-17-1361-2021](https://doi.org/10.5194/os-17-1361-2021)  
  *Relevance:* Assimilating observational spill polygons into backward/forward advective particle dispersion ensembles.

* **Kumar, R. R., Prasad, K. V. S. R., & Shenoi, S. S. C. (2017).**  
  *Online Oil Spill Advisory system for Indian Ocean.*  
  *Current Science*, 112(8), 1690–1697.  
  *Relevance:* Operational trajectory modeling and regional ROMS/HYCOM hydrodynamics in the Arabian Sea and Bay of Bengal.

---

### 1.2 Synthetic Aperture Radar (SAR) Remote Sensing & Slick Physics

* **Alpers, W., & Hühnerfuss, H. (1988).**  
  *Radar signatures of oil films and other sea surface films.*  
  *Journal of Geophysical Research: Oceans*, 93(C4), 3641–3648.  
  DOI: [10.1029/JC093iC04p03641](https://doi.org/10.1029/JC093iC04p03641)  
  *Relevance:* Marangoni wave dampening theory explaining why mineral and biogenic oils reduce short capillary waves ($1\text{--}10\text{ cm}$), causing specular radar backscatter loss ($\sigma^0$ attenuation) in C-band SAR.

* **Solberg, A. H. S., Brekke, C., & Husøy, P. O. (2007).**  
  *Oil spill detection in Radarsat and Envisat SAR images.*  
  *IEEE Transactions on Geoscience and Remote Sensing*, 45(3), 746–755.  
  DOI: [10.1109/TGRS.2006.887019](https://doi.org/10.1109/TGRS.2006.887019)  
  *Relevance:* Dark-spot segmentation, slick elongation ratio, boundary gradient analysis, and feature-based look-alike discrimination.

* **Brekke, C., & Solberg, A. H. S. (2005).**  
  *Oil spill detection by satellite remote sensing.*  
  *Remote Sensing of Environment*, 95(1), 1–13.  
  DOI: [10.1016/j.rse.2004.11.015](https://doi.org/10.1016/j.rse.2004.11.015)  
  *Relevance:* Comprehensive review of meteorological operating windows for SAR: wind speed lower bounds ($u_{10} \ge 3\text{ m/s}$ to prevent mirror calm) and upper bounds ($u_{10} \le 12\text{--}14\text{ m/s}$ before vertical entrainment).

* **Topouzelis, K. (2008).**  
  *Oil spill detection by Synthetic Aperture Radar (SAR) images: dark formation detection, feature extraction and classification.*  
  *Sensors*, 8(10), 6642–6659.  
  DOI: [10.3390/s8106642](https://doi.org/10.3390/s8106642)  
  *Relevance:* Geometric and textural descriptors used in our `SlickGeometryExtractor` (major/minor axis, perimeter-to-area ratio, orientation angle $\theta$).

---

### 1.3 Bayesian Reasoning, Forensic Evidence & Adversarial Falsification

* **Popper, K. R. (1959).**  
  *The Logic of Scientific Discovery.*  
  Routledge, London. ISBN: 978-0415278447.  
  *Relevance:* Core principle of the **Adversarial Falsification Engine**: scientific attribution cannot be proven by accumulating confirming clues alone; it requires actively subjecting hypotheses to severe falsification challenges.

* **Pearl, J. (2009).**  
  *Causality: Models, Reasoning, and Inference* (2nd ed.).  
  Cambridge University Press. DOI: [10.1017/CBO9780511803161](https://doi.org/10.1017/CBO9780511803161)  
  *Relevance:* Structural causal modeling and counterfactual simulation ($Y_{X=x}$): simulating forward from a candidate ship's release point to test whether it physically reproduces the observed slick geometry.

* **Aitken, C., & Taroni, F. (2004).**  
  *Statistics and the Evaluation of Evidence for Forensic Scientists* (2nd ed.).  
  John Wiley & Sons, Chichester. DOI: [10.1002/0470011238](https://doi.org/10.1002/0470011238)  
  *Relevance:* Bidirectional evidence weighting (positive likelihood ratios vs negative likelihood ratios) and the scientific mandate to abstain (`INSUFFICIENT_EVIDENCE`) when likelihood ratios are close to unity.

* **Scott, D. W. (2015).**  
  *Multivariate Density Estimation: Theory, Practice, and Visualization* (2nd ed.).  
  John Wiley & Sons, Hoboken, NJ. DOI: [10.1002/9781118575499](https://doi.org/10.1002/9781118575499)  
  *Relevance:* Scott's rule for optimal bandwidth selection in 2D Gaussian Kernel Density Estimation (KDE) to generate smooth origin probability contours.

---

### 1.4 Information Theory, Uncertainty Quantification & Active Sensing

* **Shannon, C. E. (1948).**  
  *A Mathematical Theory of Communication.*  
  *Bell System Technical Journal*, 27(3), 379–423.  
  DOI: [10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x)  
  *Relevance:* Shannon entropy $H(\mathbf{p}) = -\sum p_i \log_2(p_i)$ used to measure attribution ambiguity across competing vessel and non-vessel hypotheses.

* **MacKay, D. J. C. (2003).**  
  *Information Theory, Inference, and Learning Algorithms.*  
  Cambridge University Press. ISBN: 978-0521642989.  
  *Relevance:* Information gain $\mathbb{E}[\Delta H(A_m)]$ for optimal experimental design and our Active Sensing Next-Best-Evidence engine.

* **Settles, B. (2012).**  
  *Active Learning.*  
  Synthesis Lectures on Artificial Intelligence and Machine Learning, Morgan & Claypool.  
  DOI: [10.2200/S00429ED1V01Y201207AIM018](https://doi.org/10.2200/S00429ED1V01Y201207AIM018)  
  *Relevance:* Expected entropy reduction criteria to direct targeted secondary surveillance assets (e.g. SAR tasking, coastal patrol flights).

---

## 2. Operational Systems & Prior Art Benchmarks

| System Name | Operating Agency | Geographic Scope | Technology Stack | Primary Reference / Link |
|---|---|---|---|---|
| **CleanSeaNet (CSN)** | European Maritime Safety Agency (EMSA) | Pan-European EEZs | Sentinel-1 SAR + SafeSeaNet AIS + Human Analyst | [EMSA CleanSeaNet Portal](https://www.emsa.europa.eu/csn-menu.html) |
| **INCOIS OOSA** | Indian National Centre for Ocean Info. Services | Indian Ocean Region | Regional ROMS / HYCOM + NOAA GNOME Solver | [INCOIS OOSA Portal](https://incois.gov.in/portal/OOSA/oosa.jsp) |
| **OpenDrift / OpenOil** | MET Norway | Global Oceans | Modular Python + NetCDF + ADIOS Chemistry | [OpenDrift Documentation](https://opendrift.github.io/) / [GitHub Repository](https://github.com/OpenDrift/opendrift) |
| **SkyTruth Cerulean** | SkyTruth (US Non-Profit) | Global Oceans | Sentinel-1 SAR + Spire/GFW AIS + Deep Learning | [SkyTruth Cerulean Platform](https://cerulean.skytruth.org/) / [Whitepaper](https://skytruth.org/cerulean/) |
| **NOAA GNOME** | NOAA Office of Response & Restoration | US Waters & Global | Lagrangian Trajectory + ADIOS Database | [NOAA GNOME Suite](https://response.restoration.noaa.gov/gnome) |

---

## 3. Satellite Remote Sensing Portals & APIs

* **Copernicus Data Space Ecosystem (CDSE)**  
  *Provider:* European Space Agency (ESA) & European Commission  
  *Description:* Primary cloud portal providing open access to raw and calibrated Sentinel-1 C-band SAR Level-1 GRD products and Sentinel-2 MSI Level-2A BOA reflectance.  
  *Access URL:* [https://dataspace.copernicus.eu/](https://dataspace.copernicus.eu/)  
  *Interactive Browser:* [https://browser.dataprocess.copernicus.eu/](https://browser.dataprocess.copernicus.eu/)

* **Alaska Satellite Facility (ASF) DAAC**  
  *Provider:* NASA Distributed Active Archive Center / University of Alaska Fairbanks  
  *Description:* Search API and Vertex portal for Synthetic Aperture Radar imagery (Sentinel-1, ALOS PALSAR, ERS-1/2, Radarsat).  
  *Access URL:* [https://asf.alaska.edu/](https://asf.alaska.edu/)

* **Microsoft Planetary Computer STAC API**  
  *Provider:* Microsoft AI for Earth  
  *Description:* Cloud-native Spatio-Temporal Asset Catalog (STAC) hosting global Sentinel-1 RTC and Sentinel-2 Level-2A GeoTIFFs.  
  *Access URL:* [https://planetarycomputer.microsoft.com/](https://planetarycomputer.microsoft.com/)

---

## 4. Oceanographic & Atmospheric Reanalysis Services

* **Copernicus Climate Data Store (CDS) — ECMWF ERA5**  
  *Provider:* European Centre for Medium-Range Weather Forecasts (ECMWF)  
  *Dataset:* ERA5 hourly data on single levels from 1940 to present ($0.25^\circ \times 0.25^\circ$ grid).  
  *Variables Used:* 10m eastward wind (`u10`), 10m northward wind (`v10`), mean sea level pressure (`msl`).  
  *Access URL:* [https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels)  
  *Python Client:* `pip install cdsapi`

* **Copernicus Marine Environment Monitoring Service (CMEMS)**  
  *Provider:* Mercator Ocean International / European Commission  
  *Dataset:* Global Ocean Physics Analysis and Forecast (`GLOBAL_ANALYSISFORECAST_PHY_001_024`) and GLORYS12 reanalysis ($1/12^\circ \approx 8\text{ km}$ resolution).  
  *Variables Used:* Surface velocity eastward (`uo`), surface velocity northward (`vo`), sea surface temperature (`tob`), wave height.  
  *Access URL:* [https://marine.copernicus.eu/](https://marine.copernicus.eu/)  
  *Python Client:* `pip install copernicusmarine`

* **NOAA Center for Operational Oceanographic Products and Services (CO-OPS)**  
  *Provider:* National Oceanic and Atmospheric Administration (NOAA)  
  *Description:* Real-time coastal oceanographic currents, tides, and meteorology across US harbors.  
  *Access URL:* [https://tidesandcurrents.noaa.gov/](https://tidesandcurrents.noaa.gov/)

* **Coastal Data Information Program (CDIP)**  
  *Provider:* Scripps Institution of Oceanography, UC San Diego  
  *Description:* High-resolution coastal swell, wave direction, and surface current measurements.  
  *Access URL:* [https://cdip.ucsd.edu/](https://cdip.ucsd.edu/)

---

## 5. Vessel Tracking & AIS Registries

* **NOAA MarineCadastre AIS**  
  *Provider:* Bureau of Ocean Energy Management (BOEM) & NOAA Coastal Services Center  
  *Coverage:* US coastal waters, territorial sea, and EEZ (2009–Present).  
  *Format:* 1-minute downsampled, quality-controlled Class A and Class B AIS tracks in CSV and GeoPackage.  
  *Access URL:* [https://marinecadastre.gov/ais/](https://marinecadastre.gov/ais/)

* **Danish Maritime Authority (DMA) Open AIS**  
  *Provider:* Ministry of Industry, Business and Financial Affairs, Denmark  
  *Coverage:* North Sea, Baltic Sea, Danish Straits, and Kattegat/Skagerrak choke points.  
  *Format:* Continuous high-frequency daily CSV transponder archives.  
  *Access URL:* [https://dma.dk/safety-at-sea/navigational-information/ais-data](https://dma.dk/safety-at-sea/navigational-information/ais-data)

* **Global Fishing Watch (GFW) Research Datasets**  
  *Provider:* Global Fishing Watch / Google Cloud Platform  
  *Coverage:* Global commercial vessel trajectories, anchor events, and transponder gap detections.  
  *Access URL:* [https://globalfishingwatch.org/datasets-and-code/](https://globalfishingwatch.org/datasets-and-code/)

---

## 6. Benchmark Incident Ground Truth & Formal Investigation Reports

### CASE_001_WAKASHIO — Pointe d'Esny, Mauritius (August 2020)
* **Incident Summary:** Fully laden capesize bulk carrier *MV Wakashio* (IMO 9337183) grounded on coastal coral reefs off Pointe d'Esny, Mauritius on July 25, 2020; the hull fractured on August 6, releasing ~1,000 metric tons of VLSFO bunker fuel into a designated Ramsar wetland.
* **Formal Accident Investigation Report:**
  * Court of Investigation (2021). *Report of the Court of Investigation into the Grounding of MV Wakashio*. Port Louis, Republic of Mauritius.
  * Panama Maritime Authority (AMP) (2020). *Preliminary Accident Investigation Report: Grounding of Bulk Carrier MV Wakashio*. Directorate General of Merchant Marine, Panama City.
* **Geospatial Assets:** Sentinel-1A SAR IW (2020-08-06T14:45:12Z), Sentinel-2 optical scenes, full high-resolution terrestrial AIS transit track (heading 238°).

---

### CASE_002_NEW_DIAMOND — Sangamankanda, Sri Lanka (September 2020)
* **Incident Summary:** Fully laden VLCC crude tanker *MT New Diamond* (IMO 9191424) carrying 270,000 metric tons of Kuwait export crude suffered an engine-room boiler explosion 38 nautical miles off Sangamankanda, Sri Lanka on September 3, 2020. Severe fires burned for days while cargo and bunker fuel leaked into the open ocean.
* **Formal Incident Reports:**
  * Marine Environment Protection Authority (MEPA) Sri Lanka & Indian Coast Guard (2020). *Joint Operational Situation Report: Salvage, Firefighting, and Marine Oil Spill Response for MT New Diamond*. Colombo, Sri Lanka.
  * International Maritime Organization (IMO) GISIS Marine Casualties Database (Incident ID: C0015891).
* **Geospatial Assets:** Sentinel-1 SAR acquisition (2020-09-04T12:30:00Z), Southwest Monsoon Current vectors (CMEMS), AIS tracks of *MT New Diamond*, salvage tugs, and passing container traffic.

---

### CASE_003_HUNTINGTON — San Pedro Bay, Huntington Beach, California (October 2021)
* **Incident Summary:** Amplify Energy offshore pipeline P00547 was displaced by up to 105 feet and ruptured following anchor strikes by the container ships *MSC Danit* and *Beijing* during a severe January 2021 Pacific storm; slow continuous weeping culminated in a massive 25,000-gallon spill detected on October 1–2, 2021.
* **Formal Accident Investigation Report:**
  * National Transportation Safety Board (NTSB) (2023). *Anchor Strike and Pipeline Rupture: San Pedro Bay, California, October 1, 2021*. Marine Accident Report **NTSB/MIR-22/23**.  
    Direct PDF: [https://www.ntsb.gov/investigations/AccidentReports/Reports/MIR2223.pdf](https://www.ntsb.gov/investigations/AccidentReports/Reports/MIR2223.pdf)
  * Pipeline and Hazardous Materials Safety Administration (PHMSA) (2021). *Corrective Action Order: CPF No. 5-2021-054-CAO*. U.S. Department of Transportation.
* **Geospatial Assets:** Sentinel-1 SAR (2021-10-02T13:50:22Z), NOAA MarineCadastre 1-minute AIS tracks, California Current hydrodynamic fields.

---

### CASE_004_ENNORE — Kamarajar Port, Chennai, India (January 2017)
* **Incident Summary:** Outbound LPG tanker *MT BW Maple* (IMO 9223784) collided with inbound petroleum tanker *MT Dawn Kanchipuram* (IMO 9114816) off Kamarajar Port, Ennore on January 28, 2017, breaching fuel tanks and spilling over 250 metric tons of heavy bunker oil into the Bay of Bengal coastline.
* **Formal Investigation Report:**
  * Directorate General of Shipping, Ministry of Shipping, Government of India (2017). *Formal Investigation Report under Section 359 of Merchant Shipping Act, 1958: Collision between MT BW Maple and MT Dawn Kanchipuram off Kamarajar Port, Ennore on 28th January 2017*. Mumbai, India.
* **Geospatial Assets:** Sentinel-1 SAR scenes (2017-01-28 and 2017-02-01), INCOIS coastal ocean forecasts, terrestrial AIS records of both colliding vessels and port tugboats.

---

### CASE_005_SYNTHETIC_CHALLENGE — Arabian Sea Adversarial Benchmark (May 2024)
* **Benchmark Specification:** Controlled multi-candidate forensic benchmark designed specifically for adversarial testing of the SIH26143 system.
* **Scenario Properties:**
  * 3 candidate merchant vessels (*Vessel Alpha*, *Vessel Beta*, *Vessel Gamma*) transiting an active shipping corridor.
  * Staggered historical release windows with analytical current advection ($u = 0.25\text{ m/s}, v = -0.15\text{ m/s}$).
  * Decoy low-wind false positive slick ($u_{10} = 2.1\text{ m/s}$) to test look-alike meteorological rejection.
  * Deliberate 3.5-hour AIS transponder gap on candidate *Vessel Gamma* to validate AIS silence falsification.

---

## 7. International Standards, Treaties & Technical Specifications

* **IMO MARPOL 73/78 (International Convention for the Prevention of Pollution from Ships)**  
  *Annex I:* Regulations for the Prevention of Pollution by Oil.  
  *Regulation 15 & 34:* Discharge criteria governing operational machinery space bilge discharges and cargo tank washings (maximum oil content of effluent $\le 15\text{ ppm}$, prohibition of discharge within 50 nautical miles of land for tankers).  
  *Reference:* [IMO MARPOL Convention](https://www.imo.org/en/About/Conventions/Pages/International-Convention-for-the-Prevention-of-Pollution-from-Ships-(MARPOL).aspx)

* **IMO SOLAS Convention (Safety of Life at Sea)**  
  *Chapter V, Regulation 19:* Mandatory carriage requirements for shipborne automatic identification systems (Class A AIS for all ships $\ge 300\text{ GT}$ on international voyages and all passenger ships).

* **ITU-R M.1371-5 (Technical Characteristics for an Automatic Identification System)**  
  *Standard:* International Telecommunication Union specification for VHF data exchange systems using time-division multiple access (TDMA) in the maritime mobile band.  
  *Reference:* [ITU-R Recommendation M.1371-5](https://www.itu.int/rec/R-REC-M.1371/)

* **ISO/IEC 17025:2017 (General Requirements for the Competence of Testing and Calibration Laboratories)**  
  *Standard:* Forensic uncertainty quantification, evidence chain of custody, measurement traceability, and strict criteria for reporting scientific inconclusive findings / honest abstention.

* **OGC GeoJSON Format Specification (IETF RFC 7946)**  
  *Specification:* Geographic JSON encoding for geometry objects (Point, LineString, Polygon, FeatureCollection) utilized across all internal spatial APIs.  
  *Reference:* [RFC 7946 Standard](https://datatracker.ietf.org/doc/html/rfc7946)

---
*Catalog maintained as part of the SIH26143 Maritime Forensic Intelligence Engine project repository.*
