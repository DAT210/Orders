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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/order", methods=["POST"])
def order():
    i = random.randint(1, 100000)
    productID = request.form.get("ProductID")
    orderTime = request.form.get("OrderTime")
    paymentMethod = request.form.get("PaymentMethod")
    CustomerID = request.form.get("CustomerID")
    deliveryMethod = request.form.get("DeliveryMethod")
    price = request.form.get("Price")
    checkIfPaid = request.form.get("Payed")

    OrderInsert = "INSERT INTO Orders(ProductID, CustomerID, PaymentMethod, DeliveryMethod, Price, Payed)" \
                  "VALUES(%s, %s ,'%s','%s' ,%s ,%s)" % (productID, CustomerID, paymentMethod, deliveryMethod, price, 1)
    ProductInsert = "INSERT INTO Product(ProductID) VALUES(%s);" % productID

    cur.execute(ProductInsert)
    cur.execute(OrderInsert)
    conn.commit()
    return render_template("index.html")


@app.route("/order/<int:OrderID>", methods=["GET"])
def getorder(OrderID):
    query = "SELECT * FROM Orders WHERE OrderID = %s;" % OrderID
    cur.execute(query)
    Order = cur.fetchall()
    conn.commit()

    OrderID = OrderID
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
