var name = document.getElementById("eName");
var start = document.getElementById("start");
var end = document.getElementById("end");
var date = new Date()
var offset = date.getTimezoneOffset();
date.setMinutes(date.getMinutes()-offset-1);
date = date.toISOString().split('.')[0];

function nameTaken() {
    alert("Event name is already taken");
    name.style.backgroundColor = "red";
}
function check() {
    if(end.value < start.value || (start.value + ":00") < date){
        alert("Dates do not make sense")
        start.style.backgroundColor = "red";
        end.style.backgroundColor = "red";
        return false;
    } else {
        return true;
    }
}
