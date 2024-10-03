import requests
import os
import base64
import json
import time
import threading
from . import constants

# Global variable to store the access token and its expiry time
access_token_cache = {
    "token": None,
    "expiry": 0
}

# Lock to prevent thundering herd problem
token_lock = threading.Lock()

def decode_jwt(token):
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

def login():
    global access_token_cache

    # Check if the token is still valid
    if access_token_cache["token"] and access_token_cache["expiry"] > time.time():
        return access_token_cache["token"]

    # Acquire the lock to ensure only one thread refreshes the token
    with token_lock:
        # Double-check if the token was refreshed while waiting for the lock
        if access_token_cache["token"] and access_token_cache["expiry"] > time.time():
            return access_token_cache["token"]

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
            decoded_token = decode_jwt(token)
            expiry = decoded_token.get("exp", 0)

            # Update the cache
            access_token_cache["token"] = token
            access_token_cache["expiry"] = expiry

            return token
        except requests.exceptions.HTTPError as http_err:
            # TODO: Add logger for HTTP errors
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            # TODO: Add logger for general errors
            raise Exception(f"An error occurred: {err}")