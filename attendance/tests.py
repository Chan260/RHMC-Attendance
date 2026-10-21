
import json
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from attendance.attendance_service_client import get_service_health


class AttendanceServiceClientTests(SimpleTestCase):

    @patch("attendance.attendance_service_client.urlopen")
    def test_get_service_health_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            "service": "attendance-service",
            "status": "healthy",
        }).encode("utf-8")

        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = get_service_health()

        self.assertEqual(result["http_status"], 200)
        self.assertEqual(
            result["data"]["service"],
            "attendance-service",
        )
        self.assertEqual(result["data"]["status"], "healthy")
