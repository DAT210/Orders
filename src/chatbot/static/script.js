$( document ).ready(function() {
    alert("works");
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
            alert(obj);
        }
    };
    xhr.open("GET", url, true);
    xhr.send(null);
    $( "#bot" ).html( "<div>doth thou worketh?<br> this isn't working is it?</div>" );
    return false;
}
