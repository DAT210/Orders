import requests
info = requests.get("http://127.0.0.1:5000/order/3")


print(info.headers)
print(info.text)
