


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
    console.log("yoyoyo");
}



function init() {
    var radios = document.getElementsByName("delMethod");
    for(var i = 0, max = radios.length; i < max; i++) {
        radios[i].onclick = DeliveryInfoArea;
    }
    console.log("hey");

}

window.onload = init;
