import os
import requests
import json


def authenticate():
    """
    Authenticate with the harpin AI API using client credentials.
    
    Returns:
        dict: The response from the API containing authentication tokens
        
    Raises:
        requests.RequestException: If the API request fails
        KeyError: If required environment variables are missing
    """
    # Get credentials from environment variables
    client_id = os.getenv('CLIENT_ID')
    refresh_token = os.getenv('REFRESH_TOKEN')
    
    # Check if required environment variables are set
    if not client_id:
        raise KeyError("CLIENT_ID environment variable is required")
    if not refresh_token:
        raise KeyError("REFRESH_TOKEN environment variable is required")
    
    # API endpoint
    url = "https://api.harpin.ai/token"
    
    # Request headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request body
    payload = {
        "clientId": client_id,
        "refreshToken": refresh_token
    }
    
    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=payload)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
        
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        raise


def main():
    """
    Example usage of the authenticate function.
    """
    try:
        result = authenticate()
        print("Authentication successful!")
        print(f"Response: {json.dumps(result, indent=2)}")
    except (KeyError, requests.RequestException) as e:
        print(f"Authentication failed: {e}")


if __name__ == "__main__":
    main()
