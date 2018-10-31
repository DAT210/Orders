from flask import Flask, request, render_template, redirect
import mysql.connector
from mysql.connector import errorcode
import json
import requests
import re

# Connect to database
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

# TODO: Look at Customer's master to see how they use JWT.
# I'm gonna try an follow the user story with these api's


# First, we get information the ingredients from menu
# Takes the information 
@app.route("/orders/api/order/neworder", methods=["POST"])
def ReceiveInfoFromMenu():
    contentjson = request.get_json(force=True)

    totalPrice = 0
    for item in contentjson:
        totalPrice += float(item["price"]) * float(item["amount"])

    insertIntoOrder = "INSERT INTO Orders(Price) VALUES(%s)" % totalPrice
    cur.execute(insertIntoOrder)
    conn.commit()

    getLatestOrderID = "SELECT MAX(OrderID) from Orders"
    cur.execute(getLatestOrderID)

    # Filter stuff
    OrderID = cur.fetchall()
    ID = re.sub("\D", "", str(OrderID[0]))

    OrderIDandTotalPrice = []
    OrderIDandTotalPrice.append({"OrderID": int(ID)})
    OrderIDandTotalPrice.append({"TotalPrice": str(totalPrice)})
    OrderIDAndTotalPriceToFrontEnd = json.dumps(OrderIDandTotalPrice)

    status = requests.post("http://localhost:5000/sendPrice/oid", json=OrderIDAndTotalPriceToFrontEnd)

    if status.status_code != 200:
        return render_template("not200error.html")

    CoursesToThomas = json.dumps(contentjson)
    status = requests.post("http://localhost:5000/sendCart", json=CoursesToThomas)

    if status.status_code == 200:
        return redirect("http://localhost:5000/orderIndex")
    else:
        return render_template("not200error.html")


# When requested for this spesific url, you get all info about the order with given ID
@app.route("/orders/api/orderID/<int:ID>", methods=["GET"])
def GetOrderByID(ID):
    OrderQuery = "SELECT * FROM Orders WHERE OrderID = %s;" % ID
    cur.execute(OrderQuery)
    Order = cur.fetchall()
    conn.commit()

    OrderID = ID
    CustomerID = Order[0][1]
    OrderTime = Order[0][2]
    PaymentMethod = Order[0][3]
    DeliveryMethod = Order[0][4]
    Price = Order[0][5]
    Payed = Order[0][6]

    return json.dumps(str(Order[0]))


if __name__ == "__main__":
    app.run(port="4000")

