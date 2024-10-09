import os

# Constants for HTTP headers
CONTENT_TYPE = "Content-Type"
APPLICATION_JSON = "application/json"
AUTH_HEADER = "auth"
API_KEY = os.environ.get("API_KEY")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SIGNING_KEY=os.environ.get("SIGNING_KEY")