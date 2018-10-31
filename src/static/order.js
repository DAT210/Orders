
function checkDeliveryPrice() {

    var xhr = new XMLHttpRequest();
    /* register an embedded function as the handler */
    xhr.onreadystatechange = function() {
        /* readyState = 4 means that the response has been completed
         * status = 200 indicates that the request was successfully completed */
        if (xhr.readyState == 4 && xhr.status == 200) {
            // TODO complete
            var result = xhr.responseText;
            if (result != 0){
                document.getElementById("deliveryPrice").innerHTML = result;
            }
            else{
                document.getElementById("deliveryPrice").innerHTML = "Error getting delivery price";
            }


        }
    };

    var address = document.getElementById("address").value;
    var city = document.getElementById("city").value;
    var zipcode = document.getElementById("zipcode").value;
    var method = document.getElementById("transMethod").value;
    var jsonThing = {"address": address, "zipcode": zipcode, "city": city, "method": method};

    console.log(zipcode);
    xhr.open("POST", "/checkDeliveryPrice", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("data="+JSON.stringify(jsonThing));
}

function DeliveryInfoArea() {
    var deliveryMethod = document.getElementsByName("delMethod");
    var selected;

    for(var i = 0; i < deliveryMethod.length; i++) {
       if(deliveryMethod[i].checked)
           selected = deliveryMethod[i].value;
    }

    if (selected == "DoorDelivery"){
        document.getElementById("deliveryInfo").style.display = "";
    }
    if (selected == "Pickup"){
        document.getElementById("deliveryInfo").style.display = "none";
    }
    console.log(selected);
}



function init() {
    var radios = document.getElementsByName("delMethod");
    for(var i = 0, max = radios.length; i < max; i++) {
        radios[i].onclick = DeliveryInfoArea;
    }
    document.getElementById("address").onblur = checkDeliveryPrice;
    document.getElementById("city").onblur = checkDeliveryPrice;
    document.getElementById("zipcode").onblur = checkDeliveryPrice;
    document.getElementById("transMethod").onblur = checkDeliveryPrice;

}

window.onload = init;
