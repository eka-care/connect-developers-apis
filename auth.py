import requests
import base64
import json
import time
import threading
from . import constants

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self):
        self.access_token_cache = {
            "token": None,
            "expiry": 0
        }
        self.token_lock = threading.Lock()

    def decode_jwt(self, token):
        # JWT token has three parts separated by dots
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid JWT token")

        # Decode the payload part (second part)
        payload = parts[1]
        # Add padding if necessary
        payload += '=' * (4 - len(payload) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_str = decoded_bytes.decode('utf-8')
        return json.loads(decoded_str)

    def _fetch_new_token(self):
        url = "https://api.eka.care/connect-auth/v1/account/login"
        payload = {
            "api_key": constants.API_KEY,
            "client_id": constants.CLIENT_ID,
            "client_secret": constants.CLIENT_SECRET,
        }
        headers = {constants.CONTENT_TYPE: constants.APPLICATION_JSON}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses (non 2xx)
            token = response.json().get("access_token")

            # Decode the token to get the expiry time
            decoded_token = self.decode_jwt(token)
            expiry = decoded_token.get("exp", 0)

            # Update the cache, subtracting 1 minute from the expiry time
            self.access_token_cache["token"] = token
            self.access_token_cache["expiry"] = expiry - 60  # Subtract 1 minute

            logger.info(f"Token refreshed successfully. Expires at {expiry - 60}")
            return token
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            raise Exception(f"An error occurred: {err}")

    def get_token(self):
        # Check if the token is still valid
        if self.access_token_cache["token"] and self.access_token_cache["expiry"] > time.time():
            return self.access_token_cache["token"]

        # Acquire the lock to ensure only one thread refreshes the token
        with self.token_lock:
            # Double-check if the token was refreshed while waiting for the lock
            if self.access_token_cache["token"] and self.access_token_cache["expiry"] > time.time():
                return self.access_token_cache["token"]

            # Fetch a new token
            return self._fetch_new_token()

# Create a global instance of TokenManager
token_manager = TokenManager()
