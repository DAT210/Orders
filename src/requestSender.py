from flask import request
import requests
import json


dict = {'question':'what is the answer?'}
jsond = json.dumps(dict)
requests.post("http://localhost:80/", json=jsond)