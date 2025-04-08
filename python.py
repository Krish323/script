- stage: SetPipelineVariablePython
  displayName: 'Set Release Variable via Python in PowerShell'
  jobs:
  - job: PowerShellPythonJob
    displayName: 'Run Python Script in PowerShell Task'
    pool:
      vmImage: 'windows-latest'
    steps:
    - powershell: |
        $env:SYSTEM_ACCESSTOKEN = "$(System.AccessToken)"
        $env:RELEASE_RELEASEID = "$(release.ReleaseId)"
        $env:PREDEPLOYGATE_SN_CHANGE_REQUEST_NUMBER = "$(PREDEPLOYGATE.SN.CHANGE_REQUEST_NUMBER)"
        $env:SYSTEM_COLLECTIONURI = "$(System.CollectionUri)"
        $env:SYSTEM_TEAMPROJECT = "$(System.TeamProject)"

        python - <<END
import os
import requests
import json

auth_token = os.environ['SYSTEM_ACCESSTOKEN']
release_id = os.environ['RELEASE_RELEASEID']
variable_name = "CC"
variable_value = os.environ.get('PREDEPLOYGATE_SN_CHANGE_REQUEST_NUMBER')
collection_uri = os.environ['SYSTEM_COLLECTIONURI']
project = os.environ['SYSTEM_TEAMPROJECT']

print(f"Updating release variable '{variable_name}' to '{variable_value}'...")

release_url = f"{collection_uri}{project}/_apis/release/releases/{release_id}?api-version=5.0"

headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}

response = requests.get(release_url, headers=headers)
release = response.json()

if variable_name not in release['variables']:
    release['variables'][variable_name] = { "value": variable_value }
else:
    release['variables'][variable_name]['value'] = variable_value

put_response = requests.put(release_url, headers=headers, data=json.dumps(release))
print(f"Variable '{variable_name}' updated. Status: {put_response.status_code}")
END
      displayName: 'Run Python Inline in PowerShell'
      env:
        SYSTEM_ACCESSTOKEN: $(System.AccessToken)