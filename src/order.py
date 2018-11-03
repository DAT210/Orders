from flask import Flask, request, render_template, redirect, Response
import json
import random
import requests


# Connect to Redis
app = Flask(__name__)

global order
order = {}
global totalPrice
totalPrice = 0
global orderID
orderID = 0

@app.route("/orderIndex", methods=["GET"])
def index():
    global order
    global totalPrice
    return render_template("orderIndex.html", order=order, total=totalPrice)

@app.route("/sendPrice/oid", methods=["POST"])
def getPriceOid():
    global totalPrice
    global orderID
    inputJSON = request.get_json(force=True)
    loaded = json.loads(inputJSON)
    totalPrice = loaded["TotalPrice"]
    orderID = loaded["OrderID"]
    return Response(status=200)

@app.route("/sendCart", methods=["POST"])
def sendCart():
    global order
    inputJSON = request.get_json(force=True)
    order = json.loads(inputJSON)
    return Response(status=200)

@app.route("/confirm", methods=["POST"])
#TODO
def confirm():
    global orderID
    deliveryMethod = request.form.get("delMethod")
    deliverType = request.form.get("transMethod")
    paymentMethod = request.form.get("payMethod")
    street = request.form.get("address")
    city = request.form.get("city")
    zipcode = request.form.get("zipcode")

    address = street+"|"+zipcode+"|"+city

    #TODO
    ##get cid from customer
    ##and make login
    cid = ""

    if deliveryMethod == "Pickup" and paymentMethod == "payOnDel":
        result = {"CustomerID": cid, "OrderID": orderID, "DeliveryMethod": "Pickup"}
        toDelivery = {"order_id": orderID, "delivery_method": "Pickup", "address": "", "aborted": False}

        dumpSelf = json.dumps(result)
        dumpDelivery = json.dumps(toDelivery)

        respSelf = requests.post("http://localhost:4000/orders/api/DeliveryMethod", json=dumpSelf) ##Send to api.py
        respDelivery = requests.post("http://localhost:4000/delivery/neworder", json=dumpDelivery)  ##send to delivery

        if respSelf.status_code == 200 and respDelivery.status_code == 200:
            return render_template("confirm.html")

    elif deliveryMethod == "Pickup" and paymentMethod == "payNow":
        # TODO
        # redirect to payment
        None

    elif deliveryMethod == "DoorDelivery" and paymentMethod == "payOnDel":
        result = {"CustomerID": cid, "OrderID": orderID, "DeliveryMethod": deliverType}
        toDelivery = {"order_id": orderID, "delivery_method": deliverType, "address": address, "aborted": False}

        dumpSelf = json.dumps(result)
        dumpDelivery = json.dumps(toDelivery)

        respSelf = requests.post("http://localhost:4000/orders/api/DeliveryMethod", json=dumpSelf)
        respDelivery = requests.post("http://localhost:4000/delivery/neworder", json=dumpDelivery)

        if respSelf.status_code == 200 and respDelivery.status_code == 200:
            return render_template("confirm.html")

    elif deliveryMethod == "DoorDelivery" and paymentMethod == "payNow":
        #TODO
        #redirect to payment
        None

    return render_template("not200error.html")

@app.route("/checkDeliveryPrice", methods=["POST"])
def checkDeliveryPrice():
    ajaxData = request.form.get("data")
    jsonData = json.loads(ajaxData)
    address = jsonData["address"]
    city = jsonData["city"]
    zipcode = jsonData["zipcode"]
    method = jsonData["method"]


    if address == "" or city == "" or zipcode == "":
        return ""

    #TODO
    #SEND REQUEST TO DELIVERY TO GET DELIVERY PRICE AND RETURN IT WITH TRAILING ",-"
    address.replace(" ", "+")
    Pricing = requests.get("http://localhost:4000/delivery/methods/eta?address="+address+"+"+zipcode+"+"+city+"&oid=<Order_ID>")
    inputJSON = json.loads(Pricing.content)

    price = 0
    eta = 0
    if method == "1":
        price = inputJSON['walking']['price']
        eta = inputJSON['walking']['eta']
    elif method == "2":
        price = inputJSON['driving']['price']
        eta = inputJSON['driving']['eta']
    elif method == "3":
        price = inputJSON['transit']['price']
        eta = inputJSON['transit']['eta']

    response = {"price": str(price)+",-", "eta": str(int(eta))+" minutes", "priceFloat": price}
    return json.dumps(response)


def calculateTotalPrice():
    total = 0
    for course in order:
        price = course["price"]
        amount = course["amount"]
        total += float(price)*float(amount)
    return total

if __name__ == "__main__":
    app.run(port=26500)
