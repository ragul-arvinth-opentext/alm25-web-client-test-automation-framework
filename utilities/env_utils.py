import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

class EnvUtils:
    @staticmethod
    def get_credentials(username):
        key = username.upper()
        encoded = os.getenv(key)
        if not encoded:
            raise ValueError(f"Missing credentials for user: {username}")
        user, password = encoded.split(":")
        return user, password