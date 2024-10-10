import os
import requests
import base64
import time
from threading import Lock
from . import constants


class RNI:
    def __init__(self):
        self.token = None
        self.expiry = 0
        self.lock = Lock()

    def get_token(self):
        # Check if the token is available and not expired without acquiring the lock
        if self.token is not None and time.time() < self.expiry:
            return self.token

        # Acquire the lock only if the token is expired or not available
        with self.lock:
            # Double-check if the token is still expired or not available
            if self.token is None or time.time() >= self.expiry:
                self.token = self._fetch_new_token()
            return self.token

    def _fetch_new_token(self):
        # Get credentials and token from environment variables
        auth = os.getenv('RNI_AUTH')
        xsrf_token = os.getenv('RNI_XSRF_TOKEN')
        
        if not auth or not xsrf_token:
            raise ValueError("RNI_AUTH and RNI_XSRF_TOKEN must set in environment variables")

        # Encode the client_id and client_secret in base64
        auth_header = f"Basic {auth}"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': auth_header,
            'Cookie': f'XSRF-TOKEN={xsrf_token}'
        }

        # Define the payload
        payload = {}

        # Make the POST request
        response = requests.post(constants.RNI_AUTH_URL, headers=headers, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data.get('access_token')
            expires_in = response_data.get('expires_in', 3600)  # Default to 1 hour if not provided
            self.expiry = time.time() + expires_in - 60  # Refresh 1 minute before expiry
            return access_token
        else:
            raise Exception(f"Failed to retrieve access token: {response.status_code} {response.text}")

    def send_data(self, data):
        headers = {
            constants.CONTENT_TYPE: constants.APPLICATION_JSON,
            'Authorization': f'Bearer {self.get_token()}'  # Add the Authorization header
        }
        
        try:
            response = requests.post(constants.RNI_SUBMIT_URL, json=data, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses (non 2xx)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # TODO: Add logger for HTTP errors
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            # TODO: Add logger for general errors
            raise Exception(f"An error occurred: {err}")

# Create a global rni instance
rni_instance = RNI()