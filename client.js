
displayView = function(){
// the code required to display a view
};
window.onload = function(){

  var view;
  var homeview;
  if (localStorage.getItem("token")) {
    view = document.getElementById("loggedinview").innerHTML;
    var info = serverstub.getUserDataByToken(localStorage.getItem("token"));

    homeview = profileInfo(info);

      document.getElementById("content").innerHTML = view;
      var oldview = document.getElementById("homeArea").innerHTML;
      document.getElementById("homeArea").innerHTML = homeview + oldview;
      functionReloadMessage();

  }else {
    document.getElementById("content").innerHTML = document.getElementById("welcomeview").innerHTML;
  }






  //code that is executed as the page is loaded.
  //You shall put your own custom code here.
  //window.alert() is not allowed to be used in your implementation.
  //window.alert("Hello TDDD97!");
};


profileInfo = function(info){

  var view = "<table style ='width:20%'>" +
    "<tr>" +
      "<th>Email: </th> <td> " + info["data"].email +" </td> " +
    "</tr>" +
    "<tr>" +
      "<th>First name: </th> <td> " + info["data"].firstname +" </td> " +
    "</tr>" +
    "<tr>" +
      "<th>Last name: </th> <td> " + info["data"].familyname +" </td> " +
    "</tr>" +
    "<tr>" +
      "<th>Gender: </th> <td> " + info["data"].gender +" </td> " +
    "</tr>" +
    "<tr>" +
      "<th>City: </th> <td> " + info["data"].city +" </td> " +
    "</tr>" +
    "<tr>" +
      "<th>Country: </th> <td> " + info["data"].country +" </td> " +
    "</tr>" +
    "</table>";

    return view;
}


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
      var message = serverstub.changePassword(localStorage.getItem("token"), oldpass, pass1);
      document.getElementById("changepswerr").innerHTML = message["message"];
    }else{
      document.getElementById("changepswerr").innerHTML = "password can't be the same as the old";
    }

  }else {
    document.getElementById("changepswerr").innerHTML = "new password don't match!";
  }

    //document.getElementById("changepswerr").innerHTML = "error here";
}


functionlogout = function(){
  localStorage.removeItem("token");
  view = document.getElementById("welcomeview").innerHTML;
  document.getElementById("content").innerHTML = view;
}

functionuploadmes = function(){
  var text = document.getElementById("submittext").value;
  console.log(text);
  var email = serverstub.getUserDataByToken(localStorage.getItem("token"))["data"].email;
  console.log(email);
  serverstub.postMessage(localStorage.getItem("token"), text, email)
  document.getElementById("submittext").value = "";
  insertText(email, text, "thewall");

}

functionReloadMessage = function()
{

  //console.log("Testing functionReloadMessage")
  var receivedText = serverstub.getUserMessagesByToken(localStorage.getItem("token"));
  var messageArray = receivedText["data"];
  var chatArea = document.getElementById("thewall");
  chatArea.innerHTML = "";
  var i = messageArray.length -1;
  for (i; i >= 0; i--) {
  //  console.log(messageArray[i].writer);
    //console.log(messageArray[i].content);
    insertText(messageArray[i].writer, messageArray[i].content, "thewall");
  }

}

insertText = function(author, text, wall)
{
 var elem = document.getElementById(wall);
 elem.innerHTML += author + ': ' + text + '\n';

}

functionBrowseUser = function()
{
  var email = document.getElementById("searchUser").value;
  //localStorage.removeItem("browse");
  localStorage.setItem("browse", email);

  info = serverstub.getUserDataByEmail(localStorage.getItem("token"), email);
  if (info["success"]) {
    //document.body.appendChild(document.getElementById("submitSearch"));
    //profileInfo(info)
    document.getElementById("browseArea").innerHTML = document.getElementById("browseProfile").innerHTML;
    document.getElementById("information").innerHTML = profileInfo(info);
  }else {
    //error message
    console.log(info["message"]);
  }



  console.log("Testing functionBrowseUser");
  console.log(document.getElementById("searchUser").value);
}

sendMessageToEmail = function(){
  var text = document.getElementById("submittexttouser").value;
  console.log(text);
  var email = localStorage.getItem("browse");
  console.log(email);
  serverstub.postMessage(localStorage.getItem("token"), text, email)
  document.getElementById("submittext").value = "";
  insertText(serverstub.getUserDataByToken(localStorage.getItem("token"))["data"].email, text, "thewallOther");
}
