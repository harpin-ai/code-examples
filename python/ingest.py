import os
import requests
import json
from authenticate import authenticate


def ingest_data(source_id, records, ingest_type="INCREMENTAL"):
    """
    Ingest data records to harpin AI.
    
    Args:
        source_id (str): The identifier of the source system
        records (list): List of data records to ingest
        ingest_type (str): Type of ingestion (INCREMENTAL, BATCH, or TEST)
    
    Returns:
        dict: The response from the API
        
    Raises:
        requests.RequestException: If the API request fails
        KeyError: If required environment variables are missing
    """
    # Get authentication token
    auth_response = authenticate()
    access_token = auth_response['accessToken']
    
    # API endpoint
    url = f"https://api.harpin.ai/sources/{source_id}/data"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Request parameters
    params = {
        "type": ingest_type
    }
    
    # Request body
    payload = {
        "data": records
    }
    
    try:
        # Make the POST request
        response = requests.post(url, headers=headers, params=params, json=payload)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
        
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        raise


def create_example_records():
    """
    Create 3 example records for ingestion.
    
    Returns:
        list: List of example records
    """
    return [
        {
            "firstName": "John",
            "lastName": "Doe",
            "emailAddress": "john.doe@example.com",
            "phoneNumber": "+1-555-123-4567",
            "streetAddress": "123 Main St",
            "city": "San Francisco",
            "governingDistrict": "CA",
            "postalCode": "94102",
            "countryCode": "US",
            "dateOfBirth": "1985-03-15",
            "accountId": "ACCT001"
        },
        {
            "firstName": "Jane",
            "lastName": "Smith",
            "emailAddress": "jane.smith@example.com",
            "phoneNumber": "+1-555-987-6543",
            "streetAddress": "456 Oak Ave",
            "city": "Los Angeles",
            "governingDistrict": "CA",
            "postalCode": "90210",
            "countryCode": "US",
            "dateOfBirth": "1990-07-22",
            "accountId": "ACCT002"
        },
        {
            "firstName": "Michael",
            "lastName": "Johnson",
            "emailAddress": "michael.johnson@example.com",
            "phoneNumber": "+1-555-456-7890",
            "streetAddress": "789 Pine Rd",
            "city": "Seattle",
            "governingDistrict": "WA",
            "postalCode": "98101",
            "countryCode": "US",
            "dateOfBirth": "1988-11-03",
            "accountId": "ACCT003"
        }
    ]


def main():
    """
    Example usage of the ingest_data function.
    """
    # You'll need to replace this with your actual source ID
    source_id = os.getenv('SOURCE_ID', 'your-source-id-here')
    
    if source_id == 'your-source-id-here':
        print("Please set the SOURCE_ID environment variable with your actual source ID")
        return
    
    try:
        # Create example records
        example_records = create_example_records()
        
        print(f"Ingesting {len(example_records)} records to source: {source_id}")
        
        # Ingest the data
        result = ingest_data(source_id, example_records)
        
        print("Ingestion successful!")
        print(f"Records received: {result.get('recordsReceived', 'N/A')}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
    except (KeyError, requests.RequestException) as e:
        print(f"Ingestion failed: {e}")


if __name__ == "__main__":
    main()
