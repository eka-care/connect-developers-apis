import requests
from . import constants


def send_data(data):
    url = "https://devapimendix.metropolisindia.com/rest/prshvtexternalapi/v1/HVT"
    headers = {constants.CONTENT_TYPE: constants.APPLICATION_JSON}
    
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