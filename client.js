
displayView = function(){
// the code required to display a view
};
window.onload = function(){

  var view;

  if (localStorage.getItem("token")) {
    view = document.getElementById("loggedinview").innerHTML;
  }else {
    view = document.getElementById("welcomeview").innerHTML;
  }
  document.getElementById("content").innerHTML = view;


  //code that is executed as the page is loaded.
  //You shall put your own custom code here.
  //window.alert() is not allowed to be used in your implementation.
  //window.alert("Hello TDDD97!");
};

functionsignup = function(){
  var pass1 = document.getElementById("passwordsignup").value;
  var pass2 = document.getElementById("repeatpsw").value;

  console.log(pass1);
  console.log(pass2);
  if (pass1 === pass2) {
    var login_object = {
      email:document.forms["signupform"]["emailsignup"].value,
      password:document.forms["signupform"]["passwordsignup"].value,
      firstname:document.forms["signupform"]["firstname"].value,
      familyname:document.forms["signupform"]["familyname"].value,
      gender:document.forms["signupform"]["gender"].value,
      city:document.forms["signupform"]["city"].value,
      country:document.forms["signupform"]["country"].value
    };
    var message = serverstub.signUp(login_object);
    document.getElementById("signuperror").innerHTML = message["message"];
    return message["success"];
  }else {
    document.getElementById("signuperror").innerHTML = "passwords don't match";
    return false;
  }
};


functionsignin = function(){
  var user = document.getElementById("emailsignin").value;
  var pass = document.getElementById("passwordsignin").value;

  console.log(user);
  console.log(pass);

  var message = serverstub.signIn(user, pass);

  document.getElementById("signinerror").innerHTML = message["message"];
  document.getElementById("signinerror").innerHTML = message["message"];

  localStorage.setItem("token", message["data"]);

  return message["success"];
};

functionHome = function(){
  document.getElementById("homeArea").style.display = "inline";
  document.getElementById("browseArea").style.display = "none";
  document.getElementById("accountArea").style.display = "none";
};
functionBrowse = function(){
  document.getElementById("homeArea").style.display = "none";
  document.getElementById("browseArea").style.display = "inline";
  document.getElementById("accountArea").style.display = "none";
};
functionAccount = function(){
  document.getElementById("homeArea").style.display = "none";
  document.getElementById("browseArea").style.display = "none";
  document.getElementById("accountArea").style.display = "inline";
};

functionchangepsw = function(){
  var oldpass = document.getElementById("oldPassword").value;
  var pass1 = document.getElementById("newPassword").value;
  var pass2 = document.getElementById("newPasswordrpt").value;

  console.log(pass1);
  console.log(pass2);
  if (pass1 === pass2) {
    if(oldpass != pass1){
      var error = serverstub.changePassword(localStorage.getItem("token"), oldpass, pass1);
      document.getElementById("changepswerr").innerHTML = error["message"];
    }else{
      document.getElementById("changepswerr").innerHTML = "password can't be the same as the old";
    }

  }else {
    document.getElementById("changepswerr").innerHTML = "new password don't match!";
  }

    //document.getElementById("changepswerr").innerHTML = "error here";
}
