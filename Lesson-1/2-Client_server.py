import requests
import json
from bearer import token 

url = 'https://the-one-api.dev/v2/quote'
headers = {
    'Accept': 'application/json',
    'Authorization': token
}


response = requests.get(url, headers = headers)
response_json = response.json()

for dialogs in response_json['docs']:
    print (dialogs['dialog'])

with open('dialogs.json', 'w') as dialogfile:
    dialogfile.write(f'{response_json}')