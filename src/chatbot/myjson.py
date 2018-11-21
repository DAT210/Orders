from flask import Flask, render_template, json, request


def availability(date):
    # TODO take the date and check it against a database
    # NB! date is a datetime obj!
    with open("fakeJson/availability.json", "r") as f:
        return json.load(f)


def price(dishName):
    with open("fakeJson/fakePrice.json", "r") as f:
        return json.load(f)
