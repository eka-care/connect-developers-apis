import requests
from .auth import login
from . import constants


def fetch_payment_details(payment_id):
    try:
        access_token = login()
    except Exception as e:
        # TODO: Add logger
        raise e

    url = f"https://api.eka.care/dr/v1/payment/transaction_status/{payment_id}"
    headers = {
        constants.CONTENT_TYPE: constants.APPLICATION_JSON,
        constants.AUTH_HEADER: access_token,
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (non 2xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # TODO: Add logger for HTTP errors
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # TODO: Add logger for general errors
        raise Exception(f"An error occurred: {err}")