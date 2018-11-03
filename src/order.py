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
def start():
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
def index():
    global order
    inputJSON = request.get_json(force=True)
    order = json.loads(inputJSON)
    return Response(status=200)

@app.route("/confirm", methods=["POST"])
#TODO
def confirm():
    deliveryMethod = request.form.get("delMethod")
    paymentMethod = request.form.get("payMethod")
    print(deliveryMethod)
    print(paymentMethod)
    return render_template("orderIndex.html")

@app.route("/checkDeliveryPrice", methods=["POST"])
def checkDeliveryPrice():
    ajaxData = request.form.get("data")
    print(ajaxData)
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
    print(Pricing.content)
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

    print(inputJSON)
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
    app.run(host='127.0.0.1', port=5000)
