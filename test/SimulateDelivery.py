import requests

jsondict = [{
        "c_id": "3",
        "c_name": "Pepperoni Pizza",
        "price": "5.20",
        "ingredients": [
            {
                "i_id": "1",
                "i_name": "Tomato Sauce"
            },

            {
                "i_id": "3",
                "i_name": "Pepperoni"
            },

            {
                "i_id": "2",
                "i_name": "Cheese"
            }

        ],
        "amount": "2"
    },

    {
        "c_id": "1",
        "c_name": "Margarita",
        "price": "5.20",
        "ingredients": [

            {
                "i_id": "1",
                "i_name": "Tomato Sauce"
            },

            {
                "i_id": "3",
                "i_name": "Cheese"
            }

        ],
        "amount": "1"
    },

    {
        "c_id": "1",
        "c_name": "Margarita",
        "price": "6.75",
        "ingredients": [

            {
                "i_id": "1",
                "i_name": "Tomato Sauce"
            },

            {
                "i_id": "1",
                "i_name": "Tomato Sauce"
            },

            {
                "i_id": "2",
                "i_name": "Cheese"
            }
        ],
        "amount": "1"
    }
]

requests.post("http://127.0.0.1:26400/orders/api/order/neworder", json=jsondict)
