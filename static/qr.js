var form = document.getElementById("qrForm");
var stuID = document.getElementById("stuID")

function check(e) {
    e.preventDefault();
    for (var i = 0; i < 6; i++) {
        if (isNaN(stuID.value.charAt(i))) {
            alert("Student ID must be valid.");
            stuID.style.backgroundColor = "red";
            return false
        }
    }
    form.submit();
}