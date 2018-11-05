from flask import Flask, request, render_template, redirect, Response, url_for
import mysql.connector
from mysql.connector import errorcode
import json
import re
import datetime

# Connect to database
app = Flask(__name__)
try:
    conn = mysql.connector.connect(
        user='root', password='Orders01', host="192.168.99.100", database='Orders', port=26306)
    cur = conn.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("invalid username/password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database does not exist')
    else:
        print(err)


# Receives information from menu, inserts it into database, and sends to our frontend.
@app.route("/orders/api/order/neworder", methods=["GET"])
def ReceiveInfoFromMenu():
    cart = request.args["cart"]
    contentjson = json.loads(cart)

    ##contentjson = request.get_json(force=True)

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
        insert = insertIntoCourses % (
            ID, item["c_id"], item["c_name"], item["amount"], item["price"])
        cur.execute(insert)
    conn.commit()

    OrderIDandTotalPrice = {"OrderID": int(ID), "TotalPrice": str(totalPrice)}
    OrderIDTotalToFrontEnd = json.dumps(OrderIDandTotalPrice)
    CoursesToFrontend = json.dumps(contentjson)
    respons = redirect("http://192.168.99.100:26500/sendCard?cart=" + CoursesToFrontend + "&orderIDtotal=" + OrderIDTotalToFrontEnd)

    if respons.status_code != 302:
        return render_template("not302.html")
    return respons


# Used if there are two courses from menu named that same, but have some tiny differences.
def IncrementCourseAmount(CourseID, OrderID):
    CourseIDQuery = "SELECT quantity FROM Courses WHERE CourseID = %s AND OrderID = %s;" % (
        CourseID, OrderID)
    cur.execute(CourseIDQuery)
    UnFilteredQuantity = cur.fetchall()
    Quantity = re.sub("\D", "", str(UnFilteredQuantity[0]))
    UpdateQuantity = "UPDATE Courses SET quantity = %s WHERE CourseID = %s AND OrderID = %s;" % (
        int(Quantity)+1, CourseID, OrderID)
    cur.execute(UpdateQuantity)
    conn.commit()


# Takes a json with OrderID and CustomerID to insert into DB
# Json should look like this: {"OrderID": <id>, "CustomerID":<id>
@app.route("/orders/api/Customer", methods=["POST"])
def InsertCustomer():
    info = request.get_json(force=True)
    InsertCustomerQuery = "UPDATE Orders Set CustomerID = %s, Paid = 1 WHERE OrderID = %s;" % (info["CustomerID"], info["OrderID"])
    cur.execute(InsertCustomerQuery)
    conn.commit()
    return Response(status=200)


# Takes a json to update database with DeliveryMethod, and maybe CustomerID, depending on where
# Json should look like this: {"CustomerID": <id>, "OrderID": <id>, "DeliveryMethod": <"method">}
@app.route("/orders/api/DeliveryMethod", methods=["POST"])
def InsertDeliveryMethod():
    info = request.get_json(force=True)
    if "CustomerID" in info:
        if info["CustomerID"] != "":
            UpdateCustomerQuery = "UPDATE Orders SET CustomerID = %s WHERE OrderID = %s;" % (
                info["CustomerID"], info["OrderID"])
            cur.execute(UpdateCustomerQuery)
            conn.commit()
    UpdateDeliveryMethodQuery = "UPDATE Orders SET DeliveryMethod = '%s' WHERE OrderID = %s;" % (
        info["DeliveryMethod"], info["OrderID"])
    cur.execute(UpdateDeliveryMethodQuery)
    conn.commit()

    return Response(status=200)


# When requested for this spesific url, you get all info about the order with given ID
@app.route("/orders/api/orderID/<int:ID>", methods=["GET"])
def GetOrderByID(ID):
    OrderQuery = "SELECT * FROM Orders WHERE OrderID = %s;" % ID
    cur.execute(OrderQuery)
    Order = cur.fetchall()
    conn.commit()
    return json.dumps(str(Order[0]))


# Get orders done by customer
@app.route("/orders/api/customerorders/<int:CustomerID>", methods=["GET"])
def GetOrdersByCustomerID(CustomerID):
    with open("parsing/Order.json", "r") as f:
        orderDict = json.load(f)

    OrderQuery = "SELECT * FROM Orders WHERE CustomerID = %s" % CustomerID
    cur.execute(OrderQuery)
    Orders = cur.fetchall()
    conn.commit()

    ListOfOrders = []
    for Order in Orders:
        for item in Order:
            key = list(orderDict.keys())[Order.index(item)]
            if isinstance(item, datetime.datetime):
                orderDict[key] = str(item)
            else:
                orderDict[key] = item
        ListOfOrders.append(orderDict)
    return json.dumps(ListOfOrders)


# Returns all courses in given OrderID
@app.route("/orders/api/courses/<int:OrderID>", methods=["GET"])
def GetCoursesFromOrderID(OrderID):
    with open("parsing/Course.json", "r") as f:
        CourseDict = json.load(f)

    CoursesQuery = "SELECT * FROM Courses WHERE OrderID = %s;" % OrderID
    cur.execute(CoursesQuery)
    Courses = cur.fetchall()
    conn.commit()

    ListOfCourses = []
    for Course in Courses:
        for item in Course:
            key = list(CourseDict.keys())[Course.index(item)]
            CourseDict[key] = item
        ListOfCourses.append(CourseDict)
    return json.dumps(ListOfCourses)


if __name__ == "__main__":
    app.run(port="80")
