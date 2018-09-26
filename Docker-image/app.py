from flask import Flask, request, render_template
import mysql.connector
import re
import random
from mysql.connector import errorcode


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


#sql = "select * from properties"
#cur.execute(sql)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/order", methods=["POST"])
def order():
    i = random.randint(1, 100000)
    productID = request.form.get("ProductID")
    orderTime = request.form.get("order_time")
    paymentMeth = request.form.get("payment_method")
    deliveryMeth = request.form.get("delivery_method")
    price = request.form.get("price")
    checkIfPaid = request.form.get("betalt")

    query = "INSERT INTO Product(Product_ID) VALUES(%s);" % (
    productID)
    global cur
    cur.execute(query)
    global conn
    conn.commit()
    return render_template("index.html")



if __name__ == "__main__":
    app.run()
