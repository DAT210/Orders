from flask import Flask, request, render_template, redirect, Response
import mysql.connector
import re
import json
import random


# Connect to Redis
app = Flask(__name__)

global order
order = {}
global totalPrice
totalPrice = 0

@app.route("/orderIndex", methods=["GET"])
def start():
    global order
    global totalPrice
    return render_template("orderIndex.html", order=order, total=totalPrice)

@app.route("/sendCart", methods=["POST"])
def index():
    global order
    global totalPrice
    inputJSON = request.get_json(force=True)
    order = json.loads(inputJSON)
    totalPrice = calculateTotalPrice()
    return Response(status=200)

@app.route("/confirm", methods=["POST"])
#TODO
def confirm():
    temp = request.form.get("delMethod")
    print(temp)
    return render_template("orderIndex.html")

@app.route("/checkDeliveryPrice", methods=["POST"])
def checkDeliveryPrice():
    ajaxData = request.form.get("data")
    print(ajaxData)
    jsonData = json.loads(ajaxData)
    address = jsonData["address"]
    city = jsonData["city"]
    zipcode = jsonData["zipcode"]

    if address == "" or city == "" or zipcode == "":
        return ""

    #TODO
    #SEND REQUEST TO DELIVERY TO GET DELIVERY PRICE AND RETURN IT WITH TRAILING ",-"

    #RETURNING DUMMY VALUE
    return str(random.randint(100, 1000))+",-"


def calculateTotalPrice():
    total = 0
    for course in order:
        price = course["price"]
        amount = course["amount"]
        total += float(price)*float(amount)
    return total

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)