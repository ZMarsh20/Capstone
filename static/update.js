var type = document.getElementById("type");
var shaft = document.getElementById("shaft");
var flex = document.getElementById("flex");
var degree = document.getElementById("degree");
var yards = document.getElementById("yards");
var extra = document.getElementById("extra");
var submit = document.getElementById("submit");
var ltype = document.getElementById("ltype");
var lshaft = document.getElementById("lshaft");
var lflex = document.getElementById("lflex");
var ldegree = document.getElementById("ldegree");
var lyards = document.getElementById("lyards");
var lextra = document.getElementById("lextra");

putter();
function putter() {
    if (type.value == "Putter") {
        flex.style.display = "none";
        degree.style.display = "none";
        yards.style.display = "none";
        lflex.style.display = "none";
        ldegree.style.display = "none";
        lyards.style.display = "none";

        flex.value = "Other";
        degree.value = "0";
        yards.value = "0";
    }
    else {
        degree.style.display = "block";
        ldegree.style.display = "block";
        flex.style.display = "block";
        lflex.style.display = "block";
        yards.style.display = "block";
        lyards.style.display = "block";
        autoDegree();
    }
}
function autoDegree() {
    switch (type.value){
        case "Driver":
            degree.value = 10.5;
            break;
        case "Wood":
        case "3-wood":
            degree.value = 15;
            break;
        case "5-wood":
            degree.value = 19;
            break;
        case "Hybrid":
        case "3-hybrid":
            degree.value = 21;
            break;
        case "5-hybrid":
            degree.value = 27;
            break;
        case "Iron":
        case "2-iron":
            degree.value = 18;
            break;
        case "3-iron":
            degree.value = 21;
            break;
        case "4-iron":
            degree.value = 24;
            break;
        case "5-iron":
            degree.value = 27;
            break;
        case "6-iron":
            degree.value = 31;
            break;
        case "7-iron":
            degree.value = 35;
            break;
        case "8-iron":
            degree.value = 38;
            break;
        case "9-iron":
            degree.value = 42;
            break;
        case "Wedge":
        case "Pitching wedge":
            degree.value = 46;
            break;
        case "Approach wedge":
            degree.value = 52;
            break;
        case "Sand wedge":
            degree.value = 56;
            break;
        case "Lob wedge":
            degree.value = 60;
            break;
    }
}
