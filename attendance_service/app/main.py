
from fastapi import FastAPI

app = FastAPI(
    title="RHMC AttendEase Attendance Service",
    description="A microservice for RHMC AttendEase attendance operations.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "service": "attendance-service",
        "status": "healthy",
    }


@app.get("/")
def home():
    return {
        "message": "RHMC AttendEase Attendance Service is running."
    }
