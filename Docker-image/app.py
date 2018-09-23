from flask import Flask, request, render_template
import mysql.connector
import re


# Connect to Redis
app = Flask(__name__)




@app.route("/")
def index():
    """Index page that shows a list of properties"""

    return render_template("index.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
