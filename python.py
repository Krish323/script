- task: UsePythonVersion@0
      inputs:
        versionSpec: '3.x'
        addToPath: true

    - script: |
        import os
        import requests
        import json

        auth_token = os.environ['SYSTEM_ACCESSTOKEN']
        release_id = os.environ['RELEASE_RELEASEID']
        variable_name = "CC"
        variable_value = os.environ.get('PREDEPLOYMENTVALIDATION_PREDEPLOYHOOK_SNOW_CHANGEREQUESTNUMBER')
        collection_uri = os.environ['SYSTEM_COLLECTIONURI']
        project = os.environ['SYSTEM_TEAMPROJECT']

        print(f"Updating release variable '{variable_name}' to '{variable_value}'...")

        release_url = f"{collection_uri}{project}/_apis/release/releases/{release_id}?api-version=5.0"

        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(release_url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        release = response.json()

        if variable_name not in release['variables']:
            release['variables'][variable_name] = { "value": variable_value }
        else:
            release['variables'][variable_name]['value'] = variable_value

        put_response = requests.put(release_url, headers=headers, data=json.dumps(release))
        put_response.raise_for_status() # Raise an exception for bad status codes
        print(f"Variable '{variable_name}' updated. Status: {put_response.status_code}")
      displayName: 'Update Release Variable Using Python'
      env:
        SYSTEM_ACCESSTOKEN: $(System.AccessToken)
        RELEASE_RELEASEID: $(release.ReleaseId)
        PREDEPLOYMENTVALIDATION_PREDEPLOYHOOK_SNOW_CHANGEREQUESTNUMBER: $(Production.PreDeploymentValidation.PreDeployHook.SNOW.ChangeRequestNumber)
        SYSTEM_COLLECTIONURI: $(System.CollectionUri)
        SYSTEM_TEAMPROJECT: $(System.TeamProject)