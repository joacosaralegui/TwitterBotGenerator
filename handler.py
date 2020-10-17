import requests
import json
from requests.exceptions import HTTPError

headers = {
    'Content-Type': 'application/json',
}

def get_response(tweet):
    data = {
        "message":tweet.full_text,
        "sender":tweet.user.name
        }

    try:
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=json.dumps(data))

        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        return jsonResponse[0]['text']

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')