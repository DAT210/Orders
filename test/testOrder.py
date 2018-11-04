
import requests
import json
from flask import Flask, request, render_template, redirect, make_response, Response, url_for, session
import os


# Connect to Redis
app = Flask(__name__)
app.secret_key = os.urandom(20000)

docker = "http://192.168.99.100:26500"
local = "http://localhost:5000"

global test_url
test_url = docker

jsondict = [{

        "c_id": "1",
        "c_name": "course alpha",
        "price": "5.20",
        "ingredients": [
            {
                "i_id": "1",
                "i_name": "ingredient alpha"
            },

            {
                "i_id": "3",
                "i_name": "ingredient charlie"
            },

            {
                "i_id": "4",
                "i_name": "ingredient delta"
            }

        ],
        "amount": "1"
    },

    {
        "c_id": "2",
        "c_name": "course alpha",
        "price": "5.20",
        "ingredients": [

            {
                "i_id": "1",
                "i_name": "ingredient alpha"
            },

            {
                "i_id": "3",
                "i_name": "ingredient charlie"
            }

        ],
        "amount": "3"
    },

    {
        "c_id": "3",
        "c_name": "course charlie",
        "price": "6.75",
        "ingredients": [

            {
                "i_id": "1",
                "i_name": "ingredient alpha"
            },

            {
                "i_id": "2",
                "i_name": "ingredient"
            }
        ],
        "amount": "4"
    }
]

total = {"OrderID": 2, "TotalPrice": 269}

deliveryPrice = {
    "driving": {
        "eta": 15.45,
        "distance": 14.317,
        "price": 132.3305
    },
    "walking": {
        "eta": 164.25,
        "distance": 12.785,
        "price": 937.025
    },
    "transit": {
        "eta": 26.766666666666666,
        "distance": 11.813,
        "price": 205.04666666666668
    }
}

@app.route("/")
def index():
    jsond = json.dumps(jsondict)
    jsondd = json.dumps(total)
    requests.post(test_url + "/sendCart", json=jsond)
    requests.post(test_url + "/sendPrice/oid", json=jsondd)
    return redirect(test_url + "/orderIndex")


@app.route("/delivery/methods/eta", methods=["GET"])
def eta():
    resp = Response(response=json.dumps(deliveryPrice), status=200, content_type=json)
    return resp


@app.route("/delivery/neworder", methods=["POST"])
def neworder():
    return make_response(Response(status=200))


@app.route("/orders/api/DeliveryMethod", methods=["POST"])
def method():
    return make_response(Response(status=200))


@app.route("/testSession")
def testSession():
    cart = json.dumps(jsondict)
    orderIDtotal = json.dumps(total)
    return redirect(test_url + "/sendCart?cart=" + cart + "&orderIDtotal=" + orderIDtotal)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)