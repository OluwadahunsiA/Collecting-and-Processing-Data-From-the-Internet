import requests
import json

url = 'https://the-one-api.dev/v2/quote'
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer iwd7iLwSup56-Ib5Rnqx '
}


response = requests.get(url, headers = headers)
response_json = response.json()

for dialogs in response_json['docs']:
    print (dialogs['dialog'])

with open('dialogs.json', 'w') as dialogfile:
    dialogfile.write(f'{response_json}')