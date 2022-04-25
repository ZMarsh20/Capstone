var eName = document.getElementById("eName");
var start = document.getElementById("start");
var end = document.getElementById("end");
var code = document.getElementById("code");
var date = new Date()
var offset = date.getTimezoneOffset();
date.setMinutes(date.getMinutes()-offset);
date.setSeconds(0);
date = date.toISOString().split('.')[0];

function nameTaken() {
    alert("Event name is already taken");
    eName.style.backgroundColor = "red";
}
function codeTaken() {
    alert("Event code taken for this time");
    code.style.backgroundColor = "red";
}

function check() {
    var diff = moment(start.value).diff(end.value, 'days');
    if(end.value <= start.value || (start.value + ":00") < date || diff > 8){
        alert("Dates do not make sense.\nMake sure they aren't in the past and the end is after the start.");
        start.style.backgroundColor = "red";
        end.style.backgroundColor = "red";
        return false;
    } else {
        return true;
    }
}
