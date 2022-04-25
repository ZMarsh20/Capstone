var form = document.getElementById("addForm");
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
function maxEvents() {
    alert("You can only have at most 5 events at any given time");
    start.style.backgroundColor = "red";
    end.style.backgroundColor = "red";
}

function check(e) {
   e.preventDefault();
    var diffTime = Math.abs(new Date(end.value) - new Date(start.value));
    var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if(end.value <= start.value || (start.value + ":00") < date || diffDays > 8){
        alert("Dates do not make sense.\nMake sure they aren't in the past and the end is after the start.");
        start.style.backgroundColor = "red";
        end.style.backgroundColor = "red";
    } else {
        form.submit();
    }
}
