# Troubleshooting Guide — SIH26143

This document provides operational diagnostics, common failure modes, and recovery procedures for the Maritime Forensic Intelligence System.

---

## 1. Environment & Setup Issues

### Issue 1: `ModuleNotFoundError: No module named 'src'`
- **Symptom:** Running standalone Python scripts in subdirectories fails with module import errors.
- **Cause:** Python execution path does not automatically include the repository root on some shells (PowerShell/cmd).
- **Resolution:**
  - Option A: Run scripts via `-m` flag from repository root:
    ```bash
    python -m experiments.setup_experiments
    ```
  - Option B: Add repository root to `PYTHONPATH`:
    ```bash
    # Windows PowerShell
    $env:PYTHONPATH = (Get-Location).Path
    # Linux / macOS
    export PYTHONPATH=$(pwd)
    ```

---

## 2. API & Frontend Issues

### Issue 2: Frontend shows blank map or network error
- **Symptom:** Map tiles fail to load or API requests return `404` or `500`.
- **Diagnostic:**
  - Check if FastAPI dev server is running on port 8000:
    ```bash
    curl http://localhost:8000/api/v1/health
    ```
  - Verify static assets are compiled:
    ```bash
    ls app/frontend/dist/
    ```
- **Resolution:**
  - If `app/frontend/dist/` is empty or missing, rebuild the frontend:
    ```bash
    cd app/frontend
    npm run build
    cd ../..
    ```
  - Restart the backend:
    ```bash
    python -m uvicorn app.api.main:app --port 8000 --reload
    ```

### Issue 3: Port 8000 already in use
- **Symptom:** `[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)`
- **Resolution:**
  - Identify process using port 8000:
    ```powershell
    Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
    ```
  - Or run on alternate port:
    ```bash
    python -m uvicorn app.api.main:app --port 8080
    ```

---

## 3. Data & Algorithmic Diagnostics

### Issue 4: Metocean JSON missing or malformed
- **Symptom:** Investigation fails with `Scenario assets not found` or Pydantic validation error.
- **Resolution:**
  - Run the analytical synthetic benchmark generator to rebuild all scenario inputs:
    ```bash
    python data/synthetic/generate_synthetic_case.py
    ```

### Issue 5: KDE origin probability matrix shows zero variance
- **Symptom:** KDE bandwidth calculation errors out or origin contours are empty.
- **Cause:** All backward particles collapsed into an identical coordinate without turbulent diffusion.
- **Resolution:**
  - Ensure horizontal diffusion is enabled ($K_h \ge 1.0\text{ m}^2/\text{s}$). In `LagrangianDriftEngine`, verify `diffusion_kh > 0`.

---

## 4. Test Suite Diagnostics
Run the full automated test suite to verify system integrity:
```bash
python -m pytest tests/ -v
```
All 38 tests should pass in under 2 seconds.
