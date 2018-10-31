from flask import Flask, request, render_template
import mysql.connector
import re
import random
from mysql.connector import errorcode
import json


# Connect to Redis
app = Flask(__name__)
try:
    conn = mysql.connector.connect(user='root', password='Orders01', host="192.168.99.100", database='Orders')
    cur = conn.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("invalid username/password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database does not exist')
    else:
        print(err)


# Accepts the json format from menu
@app.route("/api/order/new")
def from_menu():
    order = json.load(request.get_json(force=True))
    # TODO: add new OrderID for this value
    for item in order:
        customerID = item["c_id"]
        courceName = item["c_name"]
        price = item["price"]
        amount = item["amount"]
        for ingredient in order["ingredients"]:
            # TODO: maybe do something since it's a list?
            print("stuff")

# create json that the delivery people want assumes for now that we send inn all info form orderID
# and some extra that we get from thomas/customer
@app.route("/api/order/delivery", methods=["GET"])
def to_delivery():
    order = json.loads(request.get_json(force=True))
    orderID = order["OrderID"]
    customerID = order["CustomerID"]
    delivery = order["delivery"]
    deliveryPrice = delivery["price"]
    deliveryMethod = delivery["method"]
    EstTime = delivery["est_time"]
    address = delivery["address"]
    ordered = order['ordered']  # Ordered may or may not be a list of items that is ordered

    # TODO: create the json and send to delivery url
    # whatDeliveryWants = json.dumps()
    # request.post("deliveryURL", whatDeliveryWants)


@app.route("/api/order/delivery", methods=["POST"])
def from_delivery():
    print("stuff")
    # TODO: handle the json that comes from delivery, delivery price and estimated time of arrival for example


@app.route("/order", methods=["POST"])
def jsontest():
    contentjson = request.get_json(force=True)
    content = json.loads(contentjson)
    print(content["key"])
    return json.dumps(content)


# When requested for this spesific url, you get all info about the order with given ID
@app.route("/api/orderID/<int:ID>", methods=["GET"])
def getorder(ID):
    OrderQuery = "SELECT * FROM Orders WHERE OrderID = %s;" % ID
    cur.execute(OrderQuery)
    Order = cur.fetchall()
    conn.commit()

    OrderID = ID
    ProductID = Order[0][1]
    CustomerID = Order[0][2]
    OrderTime = Order[0][3]
    PaymentMethod = Order[0][4]
    PaymentMethod = Order[0][5]
    Price = Order[0][6]
    Product = Order[0][7]

    return json.dumps(str(Order[0]))


if __name__ == "__main__":
    app.run()

