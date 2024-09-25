import requests
import sys

def get_access_token(tenant_id, client_id, client_secret):
    """Retrieve an OAuth2 access token using client credentials."""
    data = {
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    # Request an OAuth2 token from Azure AD
    response = requests.post(
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        headers=headers,
        data=data,
    )
    
    # Check if we successfully retrieved a token
    if response.status_code != 200:
        print (f"Failed - Error getting token: {response.json()}")
        sys.exit(1)
    
    return response.json()["access_token"]


def get_service_principal_info(access_token, client_id):
    """Fetch the service principal information based on the client_id."""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Query the Microsoft Graph API for service principals
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=appId eq '{client_id}'",
        headers=headers,
    )
    
    # Check if the API call was successful
    if response.status_code != 200:
        print(f"Failed - Error fetching service principal: {response.json()}")
        sys.exit(1)

    
    # Return the service principal data
    service_principal_data = response.json()["value"][0]
    return service_principal_data


def display_identity_info(service_principal_data):
    """Prints the service principal details."""
    display_name = service_principal_data.get("displayName", "Unknown")
    app_id = service_principal_data.get("appId", "Unknown")
    service_principal_id = service_principal_data.get("id", "Unknown")
    
    # Output the result (similar to AWS's sts.get_caller_identity)
    print(f"DisplayName: {display_name}, AppID: {app_id}, ServicePrincipalID: {service_principal_id}")


def main():
    # Collect arguments from command-line
    tenant_id = sys.argv[1]
    client_id = sys.argv[2]
    client_secret = sys.argv[3]

    # Get the OAuth2 access token
    access_token = get_access_token(tenant_id, client_id, client_secret)
    
    # Get the service principal information
    service_principal_data = get_service_principal_info(access_token, client_id)
    
    # Display the service principal details
    display_identity_info(service_principal_data)


if __name__ == "__main__":
    main()
