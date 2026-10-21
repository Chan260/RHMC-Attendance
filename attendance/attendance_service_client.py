
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings


def get_service_health():
    """
    Check the health of the Attendance Service
    using the configured API key.
    """
    url = f"{settings.ATTENDANCE_SERVICE_URL}/health"

    request = Request(
        url,
        headers={
            "X-API-Key": settings.ATTENDANCE_SERVICE_API_KEY,
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=10) as response:
            return {
                "http_status": response.status,
                "data": json.loads(response.read().decode("utf-8")),
            }

    except HTTPError as error:
        return {
            "http_status": error.code,
            "error": "Attendance Service rejected the request.",
        }

    except (URLError, TimeoutError, OSError):
        return {
            "http_status": None,
            "error": "Could not connect to the Attendance Service.",
        }
