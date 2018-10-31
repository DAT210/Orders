## Runs multiple get requests to the api to see if we can get the correct information, with the correct json format
import json
import requests


# TODO: Create unittests for the requests

# Gets full info about a given orderID in a straight out json
Order = requests.get("http://localhost:5000/orders/api/orderid/3")
print(Order.text)

# Gets all Courses with given OrderID
Courses = requests.get("http://localhost:5000/orders/api/courses/orderid/3")
results = json.loads(str(Courses.text))


#jsonen = json.dumps(delivery)
#requests.post("http://localhost:5000/api/order/delivery", json=jsonen)