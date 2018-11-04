import unittest
import requests
import mysql.connector
from mysql.connector import errorcode


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


class MyTest(unittest.TestCase):
    # Tests getting sent the customer info and if it is properly updated in the db
    def testUpdateCustomer(self):
        requests.post("http://127.0.0.1:26400/orders/api/Customer", json={"CustomerID": 3, "OrderID": 1})
        result = CheckCustomerDatabase(3, 1)
        self.assertEqual(result, 3)

    def testUpdateDeliveryMethod(self):
        requests.post("http://127.0.0.1:26400/orders/api/Customer", json={"OrderID": 1, "DeliveryMethod": "Car"})
        result = CheckDeliveryDatabase(1, "Car")
        self.assertEqual(result, "Car")


def CheckCustomerDatabase(CustomerID, OrderID):
    Query = "SELECT %s FROM Orders WHERE OrderID = %s" % (CustomerID, OrderID)
    cur.execute(Query)
    Customer = cur.fetchall()
    return int(str(Customer)[2])


def CheckDeliveryDatabase(OrderID, Method):
    Query = "SELECT '%s' FROM Orders WHERE OrderID = %s" % (Method, OrderID)
    cur.execute(Query)
    DeliveryMethod = cur.fetchall()
    return str(DeliveryMethod)[3:6]
