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

# The api's should follow a user story, not sure how it will pan out


# Receives information from menu, inserts it into database, and sends to our frontend.
# TODO: Split into multiple methods for simplicity
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

    insertIntoCourses = "INSERT INTO Courses(OrderID, CourseID, CourseName, Quantity, Price) VALUES(%s, %s, '%s', %s, %s);"

    alreadyInserted = []
    for item in contentjson:
        if item["c_id"] in alreadyInserted:
            IncrementCourseAmount(item["c_id"], ID)
            continue
        alreadyInserted.append(item["c_id"])
        insert = insertIntoCourses % (ID, item["c_id"], item["c_name"], item["amount"], item["price"])
        cur.execute(insert)
        print(insert)
    conn.commit()

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


def IncrementCourseAmount(CourseID, OrderID):
    CourseIDQuery = "SELECT quantity FROM Courses WHERE CourseID = %s AND OrderID = %s;" % (CourseID, OrderID)
    cur.execute(CourseIDQuery)
    UnFilteredQuantity = cur.fetchall()
    Quantity = re.sub("\D", "", str(UnFilteredQuantity[0]))
    UpdateQuantity = "UPDATE Courses SET quantity = %s WHERE CourseID = %s AND OrderID = %s;" % (int(Quantity)+1, CourseID, OrderID)
    cur.execute(UpdateQuantity)
    conn.commit()


# When requested for this spesific url, you get all info about the order with given ID
@app.route("/orders/api/orderID/<int:ID>", methods=["GET"])
def GetOrderByID(ID):
    OrderQuery = "SELECT * FROM Orders WHERE OrderID = %s;" % ID
    cur.execute(OrderQuery)
    Order = cur.fetchall()
    conn.commit()

    return json.dumps(str(Order[0]))


if __name__ == "__main__":
    app.run(port="4000")

