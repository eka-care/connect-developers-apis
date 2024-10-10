import requests
from . import constants
from .auth import token_manager


def register_webhook(scope, endpoint):
    try:
        access_token = token_manager.get_token()
    except Exception as e:
        # TODO: Add logger
        raise e

    url = "https://api.eka.care/notification/v1/connect/webhook/subscriptions"
    headers = {
        constants.CONTENT_TYPE: constants.APPLICATION_JSON,
        constants.AUTH_HEADER: access_token,
    }

    data = {
        "scope": scope,
        "url": endpoint,
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (non 2xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # TODO: Add logger for HTTP errors
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # TODO: Add logger for general errors
        raise Exception(f"An error occurred: {err}")


def list_webhooks():
    try:
        access_token = token_manager.get_token()
    except Exception as e:
        # TODO: Add logger
        raise e

    url = f"https://api.eka.care/notification/v1/connect/webhook/subscriptions"
    headers = {
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


def delete_webhook(id):
    try:
        access_token = token_manager.get_token()
    except Exception as e:
        # TODO: Add logger
        raise e

    url = f"https://api.eka.care/notification/v1/connect/webhook/subscriptions/{id}"
    headers = {
        constants.AUTH_HEADER: access_token,
    }

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (non 2xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # TODO: Add logger for HTTP errors
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # TODO: Add logger for general errors
        raise Exception(f"An error occurred: {err}")


def update_webhook(id, endpoint):
    try:
        access_token = token_manager.get_token()
    except Exception as e:
        # TODO: Add logger
        raise e

    url = f"https://api.eka.care/notification/v1/connect/webhook/subscriptions/{id}"
    headers = {
        constants.CONTENT_TYPE: constants.APPLICATION_JSON,
        constants.AUTH_HEADER: access_token,
    }

    data = {
        "url": endpoint,
    }

    try:
        response = requests.patch(url, json=data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (non 2xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # TODO: Add logger for HTTP errors
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # TODO: Add logger for general errors
        raise Exception(f"An error occurred: {err}")