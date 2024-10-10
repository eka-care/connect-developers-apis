import os

# Constants for HTTP headers
CONTENT_TYPE = "Content-Type"
APPLICATION_JSON = "application/json"
AUTH_HEADER = "auth"
API_KEY = os.environ.get("API_KEY")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SIGNING_KEY=os.environ.get("SIGNING_KEY")
RNI_AUTH=os.environ.get("RNI_AUTH")
RNI_XSRF_TOKEN=os.environ.get("RNI_XSRF_TOKEN")
RNI_AUTH_URL=os.environ.get("RNI_AUTH_URL")
RNI_SUBMIT_URL=os.environ.get("RNI_SUBMIT_URL")