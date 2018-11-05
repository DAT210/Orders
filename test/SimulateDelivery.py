import requests
import json

with open("../src/parsing/OrderFromMenu.json", "r") as f:
    jsondict = json.load(f)

requests.post("http://127.0.0.1:80/orders/api/order/neworder", json=jsondict)
