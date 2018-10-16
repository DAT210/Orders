import random
import mysql.connector
from mysql.connector import errorcode


paymentMethods = ["Cash", "Credit Card", "Debit Card"]
DeliveryMethods = ["Pickup", "Car", "Drone", "Helicopter"]
Prices = [199, 299, 599, 1299]


if __name__ == "__main__":
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

    for i in range(1,16):
        j = random.randint(1, 100000)
        if i == 1:
            OrderInsert = "INSERT INTO Orders(OrderID, IngredientsID, CustomerID, PaymentMethod, DeliveryMethod, Price, Payed)" \
                  "VALUES(%s, %s, %s, '%s', '%s', %s, %s)" % (i, i, j, "Cash", "Car", "299", 1)
            ProductInsert = "INSERT INTO Ingredients(IngredientsID, Pepperoni, Cheese) VALUES(%s, '%s', '%s');" % (i, 2, 3)

        else:
            paymentMethod = random.choice(paymentMethods)
            deliveryMethod = random.choice(DeliveryMethods)
            Price = random.choice(Prices)
            OrderInsert = "INSERT INTO Orders(OrderID, IngredientsID, CustomerID, PaymentMethod, DeliveryMethod, Price, Payed)" \
                  "VALUES(%s, %s, %s, '%s', '%s', %s, %s)" % (i, i, j, paymentMethod, deliveryMethod, Price, 1)
            ProductInsert = "INSERT INTO Ingredients(IngredientsID, Pepperoni, Cheese) VALUES(%s, '%s', '%s');" % (i, random.randint(1, 4), random.randint(1, 4))

        cur.execute(ProductInsert)
        cur.execute(OrderInsert)
        conn.commit()
                
