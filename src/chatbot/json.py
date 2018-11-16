from flask import json


def availability(date):
    with open("fakeJson/availability.json", "r") as f:
        return json.load(f)


def price(dishName):
    with open("fakeJson/fakePrice.json", "r") as f:
        return json.load(f)
