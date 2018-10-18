
import requests
import json
from flask import Flask, request, render_template, redirect



# Connect to Redis
app = Flask(__name__)



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
        "amount": "2"
    }
]

@app.route("/")
def index():
    jsond = json.dumps(jsondict)
    requests.post("http://localhost:5000/sendCart", json=jsond)
    return redirect("http://localhost:5000/orderIndex")



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4000)