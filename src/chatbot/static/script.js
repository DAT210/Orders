$( document ).ready(function() {
    alert("works");
});

function ask(){
    var question = document.forms["input"]["question"].value;
    $( "#bot" ).html( "<div>doth thou worketh?<br> this isn't working is it?</div>" );
    return false;
}
