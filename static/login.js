var user = document.getElementById("user");
var username = document.getElementById("username");
var password = document.getElementById("password");
var pass = document.getElementById("pass");
var submit = document.getElementById("submit");

var newuser = document.getElementById("newuser");
var newusername = document.getElementById("newusername");
var newpassword = document.getElementById("newpassword");
var newpass = document.getElementById("newpass");
var newpassword2 = document.getElementById("newpassword2");
var newpass2 = document.getElementById("newpass2");
var submit2 = document.getElementById("submit2");
var _name = document.getElementById("name");
var lname = document.getElementById("lname");

var sign = document.getElementById("signup");
var log = document.getElementById("login");
var signupform = document.getElementById("signupform");

function signup() {
    location.assign("\\sign_up");
}
function login() {
    location.assign("\\sign_in");
}
function check() {
    if (newpassword.value === newpassword2.value) {
        if ( newusername == "" ){
            alert("Please make sure all fields are filled");
            newusername.style.backgroundColor = "red";
        } 
        else {
            if (newpassword.value == "") {
                alert("Please make sure all fields are filled");
            } else {
                return true;
            }
        }
    }
    else {
        alert("Your passwords do not match");
        newpassword.style.backgroundColor = "red";
        newpassword2.style.backgroundColor = "red";
    }
    return false;
}
function normal() {
    try {
        newpassword.style.backgroundColor = "white";
        newpassword2.style.backgroundColor = "white";
        newusername.style.backgroundColor = "white";
    } catch {
        username.style.backgroudColor = "white";
        password.style.backgroudColor = "white";
    }
}
function usernameTaken() {
    alert("Username taken or invalid. Must be a valid email.\n Please try again");
    newusername.style.backgroundColor = "red";
}
function tryAgain() {
    alert("Username or password incorrect");
    username.style.backgroundColor = "red";
    password.style.backgroundColor = "red";
}