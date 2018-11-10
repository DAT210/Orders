from flask import Flask, request, render_template, redirect, Response, session, url_for
import json
import random
import requests
import os

# Connect to Redis
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("orderIndex.html")

@app.route("/confirm")
def confirm():
    return "hey"

if __name__ == "__main__":
    app.run(port=5000)
