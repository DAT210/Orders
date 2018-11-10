import requests
import json

with open("../src/parsing/OrderFromMenu.json", "r") as f:
    jsondict = json.load(f)

requests.get("http://192.168.99.100:26400/orders/api/neworder", json=jsondict)
