# -*- encoding: utf-8 -*-

import os, requests, json
from requests.auth import HTTPBasicAuth

API_KEY = os.environ.get("SKILL_API_KEY")
ENDPOINT = os.environ.get("SKILL_ENDPOINT")
 

def getResultsByAPI(text):
    headers = {'x-api-key': API_KEY}
    payload = json.dumps({'text': text})
    r = requests.put(ENDPOINT, headers=headers, data=payload)

    return json.loads(r.content)["results"]