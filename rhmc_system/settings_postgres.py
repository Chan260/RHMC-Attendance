
from .settings import *
from dotenv import load_dotenv
import os

# Read PostgreSQL credentials from the project's .env file.
load_dotenv(BASE_DIR / ".env")

# Use PostgreSQL instead of the original MySQL database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "rhmc_attendance"),
        "USER": os.getenv("POSTGRES_USER", "rhmc_admin"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": "127.0.0.1",
        "PORT": "5433",
    }
}
