#!/usr/bin/env python3
import requests
import json
import sys
import pandas as pd
apiKey = "xxxxx-xxxx-xxx-xxxx-xxxxxxxxxx"
secretKey = "xxxx-xxx-xxx-xxxx-xxxxxxxx"

#pandas display options
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

base_url = "https://api-mobile.zscloud.net/papi"

login_url = f"{base_url}/auth/v1/login"
device_url = f"{base_url}/public/v1/getDevices"

payload = json.dumps({
  "apiKey": apiKey,
  "secretKey": secretKey
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.post(login_url, headers=headers, data=payload)
token = json.loads(response.text).get("jwtToken")

headers = {
  'auth-token': f'{token}'
}

all_devices = pd.DataFrame()

page = 1
while True:
    paginated_url = f"{device_url}?pageSize=5000&page={page}"
    device_response = requests.get(paginated_url, headers=headers)
    devices = json.loads(device_response.text)
    if not devices:
        break
    all_devices = pd.concat([all_devices, pd.DataFrame(devices)], ignore_index=True)
    page += 1

all_devices.to_csv(sys.stdout, index=False)
