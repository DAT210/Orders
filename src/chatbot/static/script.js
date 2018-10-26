$( document ).ready(function() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status== 200){
        }
    };
    xhr.open("GET", "/init", true);
    xhr.send(null);
});

function ask(){
    var question = document.forms["input"]["question"].value;
    var url = "/respond?sentence=" + question;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status== 200){
            var result = xhr.responseText;
            var obj = JSON.parse(result);
            $( "#bot" ).html( "<div>" + obj + "</div>" );
        }
    };
    xhr.open("GET", url, true);
    xhr.send(null);
    return false;
}
