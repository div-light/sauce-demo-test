import os

from dotenv import load_dotenv

load_dotenv()
HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
