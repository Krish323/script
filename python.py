import os
import requests
import json

# Access environment variables passed as arguments
auth_token = os.environ.get('SYSTEM_ACCESSTOKEN')
release_id = os.environ.get('RELEASE_RELEASEID')
variable_name = "CC"
variable_value = os.environ.get('PREDEPLOYMENTVALIDATION_PREDEPLOYHOOK_SNOW_CHANGEREQUESTNUMBER')
collection_uri = os.environ.get('SYSTEM_COLLECTIONURI')
project = os.environ.get('SYSTEM_TEAMPROJECT')

print(f"Updating release variable '{variable_name}' to '{variable_value}'...")
print(f"Release ID: {release_id}") # Debugging
print(f"Change Request Number (from env): {variable_value}") # Debugging

if not all([auth_token, release_id, collection_uri, project]):
    print("Error: One or more required environment variables are not set.")
    exit(1)

release_url = f"{collection_uri}{project}/_apis/release/releases/{release_id}?api-version=5.0"

headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}

try:
    response = requests.get(release_url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    release = response.json()

    if 'variables' not in release:
        release['variables'] = {}

    if variable_name not in release['variables']:
        release['variables'][variable_name] = {"value": variable_value}
    else:
        release['variables'][variable_name]['value'] = variable_value

    put_response = requests.put(release_url, headers=headers, data=json.dumps(release))
    put_response.raise_for_status()
    print(f"Variable '{variable_name}' updated. Status: {put_response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
    exit(1)
except KeyError as e:
    print(f"Error accessing JSON data: {e}")
    exit(1)