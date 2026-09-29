"""Health and status endpoint router."""
from fastapi import APIRouter
from datetime import datetime, timezone
import sys

router = APIRouter(prefix="/health", tags=["System Health"])

@router.get("")
def get_health():
    return {
        "status": "healthy",
        "system": "SIH26143 Maritime Forensic Intelligence Engine",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "demo_mode": True
    }
