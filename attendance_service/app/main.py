
import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader


app = FastAPI(
    title="RHMC AttendEase Attendance Service",
    description="A microservice for RHMC AttendEase attendance operations.",
    version="1.0.0",
)

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def verify_api_key(api_key: str | None = Security(api_key_header)):
    expected_api_key = os.getenv("ATTENDANCE_SERVICE_API_KEY")

    if not expected_api_key:
        raise HTTPException(
            status_code=503,
            detail="Attendance Service API key is not configured.",
        )

    if not api_key or not secrets.compare_digest(
        api_key, expected_api_key
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key.",
        )


@app.get("/health", dependencies=[Depends(verify_api_key)])
def health_check():
    return {
        "service": "attendance-service",
        "status": "healthy",
    }


@app.get("/", dependencies=[Depends(verify_api_key)])
def home():
    return {
        "message": "RHMC AttendEase Attendance Service is running."
    }



@app.get("/attendance/summary", dependencies=[Depends(verify_api_key)])
def attendance_summary(present: int = 0, absent: int = 0):
    if present < 0 or absent < 0:
        raise HTTPException(
            status_code=400,
            detail="Attendance counts cannot be negative.",
        )

    total = present + absent

    return {
        "present": present,
        "absent": absent,
        "total": total,
        "message": (
            "No attendance records found."
            if total == 0
            else f"{total} attendance records summarized."
        ),
    }
