import os
from dotenv import load_dotenv

# Load variables from .env (should be in your `utilities` folder)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

class EnvUtils:
    @staticmethod
    def get_credentials(username):
        key = username.upper()
        encoded = os.getenv(key)
        if not encoded:
            raise ValueError(f"Missing credentials for user: {username}")
        user, password = encoded.split(":")
        return user, password

    @staticmethod
    def get_base_url():
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise ValueError("BASE_URL not found in .env")
        return base_url