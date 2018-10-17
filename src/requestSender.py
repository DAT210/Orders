from flask import request
import requests
import json


dict = {'question':'what is the answer?'}
jsond = json.dumps(dict)
requests.post("http://localhost:5000/", json=jsond)