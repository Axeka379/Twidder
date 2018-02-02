
displayView = function(){
// the code required to display a view
};
window.onload = function(){

  var view = document.getElementById("welcomeview").innerHTML;
  document.getElementById("content").innerHTML = view;
  //code that is executed as the page is loaded.
  //You shall put your own custom code here.
  //window.alert() is not allowed to be used in your implementation.
  //window.alert("Hello TDDD97!");
};

functionsignup = function(){
  var pass1 = document.getElementById("passwordsignup").value;
  var pass2 = document.getElementById("repeatpsw").value;
  /*var emailsignup = document.getElementById("emailsignup").value;
  var firstnamesignup = document.getElementById("firstname").value
  var familynamesignup =
  var gendersignup =
  var citysignup =
  var countrysignup =
  */
  console.log(pass1);
  console.log(pass2);
  if (pass1 === pass2) {
    var login_object = {
      'email':document.getElementById("emailsignup").value,
      'password':document.getElementById("passwordsignup").value,
      'firstname':document.getElementById("firstname").value,
      'familyname':document.getElementById("familyname").value,
      'gender':document.getElementById("gender").value,
      'city':document.getElementById("city").value,
      'country':document.getElementById("country").value
    };
    var message = serverstub.signUp(login_object);
    document.getElementById("signuperror").innerHTML = message;
    return true;
  }else {
    document.getElementById("signuperror").innerHTML = "password don't match";
    return false;
  }
};
