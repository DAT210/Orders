from flask import json


def price(dishName):
    info = makefakejson(dishName)
    return info['price']


def makefakejson(dishname):
    # instead of getting json from another group
    dict = getList()
    if dict['c_name'] == dishname:
        return dict


def getList():
    with open("static/fakePrice.json", "r") as f:
        return json.load(f)
