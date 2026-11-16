import os

from dotenv import load_dotenv

load_dotenv()
HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "yes", "1")
BASE_URL = os.getenv("BASE_URL")
SAUCE_USERNAME = os.getenv("SAUCE_USERNAME")
PASSWORD = os.getenv("PASSWORD")
