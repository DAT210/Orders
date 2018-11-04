import unittest
import requests
import mysql.connector
from mysql.connector import errorcode
import json
import datetime

CoursesInOrder = '[{"OrderID": 1, "CourseID": 2, "CourseName": "Pepperoni", "Quantity": 3, "Price": 6.35}, ' \
                     '{"OrderID": 1, "CourseID": 2, "CourseName": "Pepperoni", "Quantity": 3, "Price": 6.35}]'

OrdersFromCustomer = '[{"OrderID": 3, "CustomerID": 1, "OrderTime": "", "PaymentMethod": "Credit",' \
                     ' "DeliveryMethod": "Pickup", "Price": 9.2, "Payed": ""}, {"OrderID": 3, "CustomerID": 1,' \
                     ' "OrderTime": "2018-11-04 18:06:07", "PaymentMethod": "Credit", "DeliveryMethod": "Pickup",' \
                     ' "Price": 9.2, "Payed": ""}]'

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
    # Tests if sending a json to this url updates the Customer info in the db at the correct OrderID
    def testUpdateCustomer(self):
        requests.post("http://127.0.0.1:80/orders/api/Customer", json={"OrderID": 1, "CustomerID": 1})
        result = CheckCustomerDatabase(1, 1)
        self.assertEqual(result, 1)

    # Tests if inserting the json updated the database at the right OrderID
    def testUpdateDeliveryMethod(self):
        requests.post("http://127.0.0.1:80/orders/api/DeliveryMethod", json={"OrderID": 1, "DeliveryMethod": "Car"})
        result = CheckDeliveryDatabase(1, "Car")
        self.assertEqual(result, "Car")

    # Checks if we get all the courses in an order (this is dependent on a static db)
    def testCoursesInOrders(self):
        result = requests.get("http://127.0.0.1:80/orders/api/courses/1")
        self.assertEqual(result.text, CoursesInOrder)

    # Checks if we get all the orders done by a customer (this is dependen on a static db)
    def testOrdersDoneByCustomer(self):
        result = requests.get("http://127.0.0.1:80/orders/api/customerorders/1")
        wanted = CheckOrdersDoneByCustomer(1)
        self.assertEqual(result.text, wanted)


def CheckCustomerDatabase(CustomerID, OrderID):
    Query = "SELECT %s FROM Orders WHERE OrderID = %s;" % (CustomerID, OrderID)
    cur.execute(Query)
    Customer = cur.fetchall()
    return int(str(Customer)[2])


def CheckDeliveryDatabase(OrderID, Method):
    Query = "SELECT '%s' FROM Orders WHERE OrderID = %s;" % (Method, OrderID)
    cur.execute(Query)
    DeliveryMethod = cur.fetchall()
    return str(DeliveryMethod)[3:6]


def CheckOrdersDoneByCustomer(CustomerID):
    with open("../src/parsing/Order.json", "r") as f:
        orderDict = json.load(f)
    Query = "SELECT * FROM Orders WHERE CustomerID = %s" % CustomerID
    cur.execute(Query)
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
