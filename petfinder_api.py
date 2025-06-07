import os                    # For accessing environment variables
import requests              # For making HTTP requests to the Petfinder API
from dotenv import load_dotenv  # Loads environment variables from a .env file

# Load environment variables from .env (e.g., PETFINDER_API_KEY, PETFINDER_SECRET)
load_dotenv()

# ===========================
#       API CREDENTIALS
# ===========================

# Your Petfinder API key and secret, stored in a .env file for security
API_KEY = os.getenv("PETFINDER_API_KEY")
API_SECRET = os.getenv("PETFINDER_SECRET")

# Petfinder API URLs
TOKEN_URL = "https://api.petfinder.com/v2/oauth2/token"
ANIMALS_URL = "https://api.petfinder.com/v2/animals"

# Data required to get an OAuth2 access token
token_data = {
    "grant_type": "client_credentials",
    "client_id": API_KEY,
    "client_secret": API_SECRET
}

# ===========================
#       API FUNCTIONS
# ===========================

def get_token():
    """Request an access token from Petfinder API using client credentials"""
    resp = requests.post(TOKEN_URL, data=token_data)  # POST request to get the token
    resp.raise_for_status()  # Raise an error if something went wrong
    return resp.json()["access_token"]  # Return the token string

def get_dogs(token, params=None):
    """
    Get a list of adoptable dogs from Petfinder API.
    
    token: OAuth2 token string
    params: dictionary of filter/search parameters
    """
    headers = {"Authorization": f"Bearer {token}"}  # Attach token to the request
    url = f"{ANIMALS_URL}?type=dog"  # Base URL for dog search

    # Append query parameters if provided (e.g., breed, age, location)
    if params:
        for key, value in params.items():
            url += f"&{key}={value}"

    resp = requests.get(url, headers=headers)  # Send GET request with token
    resp.raise_for_status()  # Raise error if API call fails
    return resp.json()["animals"]  # Return list of dog dictionaries
