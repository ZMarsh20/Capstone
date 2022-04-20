var form = document.getElementById("viewForm")
var age1 = document.getElementById("ageStart");
var age2 = document.getElementById("ageEnd");
var grad1 = document.getElementById("gradStart");
var grad2 = document.getElementById("gradEnd");

function check(e) {
   e.preventDefault();
    if (parseInt(age1.value) <= parseInt(age2.value) || (!age1.value && !age2.value)) {
        if (parseInt(grad1.value) <= parseInt(grad2.value) || (!grad1.value && !grad2.value)) {
            form.submit();
        } else {
            alert("Grad range doesn't make sense.");
            grad1.style.backgroundColor = "red";
            grad2.style.backgroundColor = "red";
        }
    } else {
        alert("Age range doesn't make sense.");
        age1.style.backgroundColor = "red";
        age2.style.backgroundColor = "red";
    }
}