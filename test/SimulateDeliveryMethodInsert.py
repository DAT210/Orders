import requests

theJson = {"CustomerID": 6, "OrderID": 15, "DeliveryMethod": "Transit"}
info = requests.post("http://127.0.0.1:26400/orders/api/DeliveryMethod", json=theJson)
print(info)

