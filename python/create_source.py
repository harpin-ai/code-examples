import os
import requests
import json
from authenticate import authenticate


def create_source(source_name, description="Identity data source"):
    """
    Create a new source for IDENTITY data with data mappings.
    
    Args:
        source_name (str): The name of the source to create
        description (str): Description of the source
    
    Returns:
        dict: The response from the API containing source details
        
    Raises:
        requests.RequestException: If the API request fails
        KeyError: If required environment variables are missing
    """
    # Get authentication token
    auth_response = authenticate()
    access_token = auth_response['accessToken']
    
    # API endpoint
    url = "https://api.harpin.ai/sources"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Data mappings that match the attribute names in ingest.py
    attribute_mappings = [
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "accountId",
            "canonicalAttribute": "sourceRecordId"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "firstName",
            "canonicalAttribute": "firstName"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "lastName",
            "canonicalAttribute": "lastName"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "emailAddress",
            "canonicalAttribute": "emailAddress"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "phoneNumber",
            "canonicalAttribute": "phoneNumber"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "streetAddress",
            "canonicalAttribute": "streetAddress"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "city",
            "canonicalAttribute": "city"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "governingDistrict",
            "canonicalAttribute": "governingDistrict"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "postalCode",
            "canonicalAttribute": "postalCode"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "countryCode",
            "canonicalAttribute": "countryCode"
        },
        {
            "domainType": "IDENTITY",
            "sourceAttribute": "dateOfBirth",
            "canonicalAttribute": "dateOfBirth"
        }
    ]
    
    # Request body
    payload = {
        "name": source_name,
        "description": description,
        "sourceSystem": "customIntegration",
        "category": "API Test",
        "domainType": "IDENTITY",
        "attributeMappings": attribute_mappings
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


def enable_source(source_id):
    """
    Enable a source by its ID.
    
    Args:
        source_id (str): The ID of the source to enable
    
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
    url = f"https://api.harpin.ai/sources/{source_id}/enabled"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "enabled": True
    }
    
    try:
        # Make the PUT request
        response = requests.put(url, headers=headers, json=payload)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
        
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        raise


def create_and_enable_source(source_name, description="Identity data source"):
    """
    Create and enable a new IDENTITY source with data mappings.
    
    Args:
        source_name (str): The name of the source to create
        description (str): Description of the source
    
    Returns:
        dict: The response containing source details and enable status
        
    Raises:
        requests.RequestException: If the API request fails
        KeyError: If required environment variables are missing
    """
    try:
        # Create the source
        print(f"Creating source: {source_name}")
        create_response = create_source(source_name, description)
        
        source_id = create_response.get('id')
        if not source_id:
            raise ValueError("Source creation failed - no ID returned")
        
        print(f"Source created successfully with ID: {source_id}")
        
        # Enable the source
        print(f"Enabling source: {source_id}")
        enable_response = enable_source(source_id)
        
        print("Source enabled successfully!")
        
        return {
            "source": create_response,
            "enabled": enable_response
        }
        
    except (requests.RequestException, ValueError) as e:
        print(f"Failed to create and enable source: {e}")
        raise


def main():
    """
    Example usage of the create_and_enable_source function.
    """
    # Get source name from environment variable or use default
    source_name = os.getenv('SOURCE_NAME', 'Identity Data Source')
    description = os.getenv('SOURCE_DESCRIPTION', 'Source for identity data ingestion with harpin AI')
    
    try:
        # Create and enable the source
        result = create_and_enable_source(source_name, description)
        
        print("\n=== Source Creation Complete ===")
        print(f"Source ID: {result['source'].get('id')}")
        print(f"Source Name: {result['source'].get('name')}")
        print(f"Data Type: {result['source'].get('dataType')}")
        print(f"Status: {'Enabled' if result['enabled'] else 'Created but not enabled'}")
        
        # Display data mappings
        mappings = result['source'].get('dataMappings', [])
        if mappings:
            print(f"\nData Mappings ({len(mappings)} total):")
            for mapping in mappings:
                print(f"  {mapping.get('sourceAttribute')} -> {mapping.get('targetAttribute')}")
        
        print(f"\nFull response: {json.dumps(result, indent=2)}")
        
        # Save source ID to environment for easy reference
        source_id = result['source'].get('id')
        print(f"\nTo use this source for ingestion, set:")
        print(f"export SOURCE_ID={source_id}")
        
    except (KeyError, requests.RequestException, ValueError) as e:
        print(f"Source creation failed: {e}")


if __name__ == "__main__":
    main()
