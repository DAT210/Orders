from flask import Flask, request, render_template
import mysql.connector
import re
import json


# Connect to Redis
app = Flask(__name__)




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



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)