from flask import Flask, request, render_template, redirect, Response, session, url_for
import json
import random
import requests
import os

# Connect to Redis
app = Flask(__name__)
app.secret_key = os.urandom(20000)


docker = "http://192.168.99.100:26300"
local = "http://localhost:3000"

global test_url
test_url = docker

@app.route("/")
def start():
    return "hello world"


@app.route("/sendCart", methods=["GET"])
def sendCart():
    cart = request.args["cart"]
    orderIDtotal = request.args["orderIDtotal"]
    orderIDtotal = json.loads(orderIDtotal)
    if orderIDtotal:
        session["cart"] = cart
    else:
        render_template("not200error.html")

    if orderIDtotal:
        session["orderID"] = orderIDtotal["OrderID"]
        session["TotalPrice"] = orderIDtotal["TotalPrice"]
    else:
        render_template("not200error.html")

    return redirect(url_for(".index"))


@app.route("/orderIndex", methods=["GET"])
def index():
    if "cart" in session and "TotalPrice" in session:
        message1 = session["cart"]
        order = json.loads(message1)
        totalPrice = session["TotalPrice"]
        return render_template("orderIndex.html", order=order, total=totalPrice)

    return render_template("woopsError.html")


@app.route("/confirm", methods=["POST"])
#TODO
def confirm():
    global test_url
    orderID = session["orderID"]
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

        respSelf = requests.post(test_url + "/orders/api/DeliveryMethod", json=dumpSelf) ##Send to api.py
        respDelivery = requests.post(test_url + "/delivery/neworder", json=dumpDelivery)  ##send to delivery

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

        respSelf = requests.post(test_url + "/orders/api/DeliveryMethod", json=dumpSelf)
        respDelivery = requests.post(test_url + "/delivery/neworder", json=dumpDelivery)

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
    Pricing = requests.get(test_url + "/delivery/methods/eta?address=" + address + "+" + zipcode + "+" + city + "&oid=<Order_ID>")
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

    response = {"price": price, "eta": str(int(eta))+" minutes", "priceFloat": price}
    return json.dumps(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
