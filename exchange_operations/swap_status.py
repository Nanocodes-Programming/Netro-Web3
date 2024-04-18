import requests
import json

#Track id is return from swap operation
def get_status(track_id: str) :
    url = "https://api.changenow.io/v2/exchange/by-id" +'?id=' + track_id

    payload = {}
    headers = {
        'x-changenow-api-key': "d9872c64579f8880ee9da4e78a48af7ef368c4dc5f9c1e5bd2b8a606b64c0d86",
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    print (response.text)
    dat = json.loads(response.text)
    status = dat['status']
    return status, response.text

