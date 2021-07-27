import requests
import json

def getRepo(USERNAME):
    header = {
    "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    url = f'https://api.github.com/users/{USERNAME}/repos'
    response = requests.get(url, headers = header)
    result = response.json()

    # Save result in json
    with open('see.json', 'w') as outfile:
        outfile.write(f'{result}')
    return result





        