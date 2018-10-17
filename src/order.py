from flask import Flask, request, render_template
import mysql.connector
import re
import json
import random


# Connect to Redis
app = Flask(__name__)



@app.route("/start", methods=["GET"])
def start():
    return render_template("orderIndex.html")
@app.route("/", methods=["POST"])
def index():

    inputJSON = request.get_json(force=True)
    inputDict = json.loads(inputJSON)
    print(inputDict["question"])
    return render_template("orderIndex.html", order=inputJSON)

@app.route("/confirm", methods=["POST"])
def confirm():

    temp = request.form.get("delMethod")
    print(temp)
    return render_template("orderIndex.html")

@app.route("/checkDeliveryPrice", methods=["POST"])
def checkDeliveryPrice():
    ajaxData = request.form.get("data")
    print(ajaxData)
    jsonData = json.loads(ajaxData)
    address = jsonData["address"]
    city = jsonData["city"]
    zipcode = jsonData["zipcode"]

    if address == "" or city == "" or zipcode == "":
        return ""

    #TODO
    #SEND REQUEST TO DELIVERY TO GET DELIVERY PRICE AND RETURN IT WITH TRAILING ",-"

    #RETURNING DUMMY VALUE
    return str(random.randint(100, 1000))+",-"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)