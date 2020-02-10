
displayView = function(){
// the code required to display a view
};

window.onbeforeunload = function(){
  //functionlogout();
}

var userEmail = null;

window.onload = function(){

  var view;
  var homeview;
  token = localStorage.getItem("token")
  if (token) {
    view = document.getElementById("loggedinview").innerHTML;

    var login_object = {
      "email":""
    };
    var info;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        info = JSON.parse(xhttp.responseText);
        homeview = profileInfo(info);
        document.getElementById("content").innerHTML = view;
        var oldview = document.getElementById("homeArea").innerHTML;
        document.getElementById("homeArea").innerHTML = homeview + oldview;
        chartUsers = initChart(0, 0, "online", "offline", "doughnut-chart", "number of people online/offline");
        chartUsersGender = initChart(0, 0, "male", "female", "doughnut-chart-gender", "Amount of male/female");
        console.log("khasdhask " + info["Success"]);
        console.log("hej " + info["data"]["email"]);
        conSocket(info["data"]["email"]);
        login_object["email"] = info["data"]["email"];

        var data;
        var xhttp2 = new XMLHttpRequest();
        xhttp2.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(xhttp2.responseText);


          }
        };
        xhttp2.open("POST", "/reload", true);
        xhttp2.setRequestHeader("Content-Type", "application/json");
        xhttp2.send(JSON.stringify(login_object));

      }
    };
    xhttp.open("GET", "/databytoken", true);
    xhttp.setRequestHeader("token", localStorage.getItem("token"));
    xhttp.send();

    functionReloadMessage();
    //var info = serverstub.getUserDataByToken(localStorage.getItem("token"));

    /*homeview = profileInfo(info);

      document.getElementById("content").innerHTML = view;
      var oldview = document.getElementById("homeArea").innerHTML;
      document.getElementById("homeArea").innerHTML = homeview + oldview;
      functionReloadMessage();
      */

  }else {
    document.getElementById("content").innerHTML = document.getElementById("welcomeview").innerHTML;
  }




};


profileInfo = function(info){


  localStorage.setItem("email", info["data"].email);
  //var cUser = Handlebars.compile(info["data"]);
  var someData = info["data"];
  //console.log(Handlebars.registerHelper('somedata', someData));
  //console.log(somedata2);
  //someData = Handlebars.compile(somedata2);
  //console.log(someData);


  //var cM = Handlebars.compile(someData);
  //console.log("BITCH");
  var template = Handlebars.compile("Handlebars {{doesWhat}}</b>");
  console.log(template({doesWhat: info["data"].email }));

  var view = Handlebars.compile("<table style ='width:20%'>" +
    "<tr>" +
      "<th>Email: </th> <td> {{email}} </td> </tr> <tr><th>First name: </th> <td> {{firstname}}" +
      "</td></tr><tr><th>Last name: </th> <td> {{lastname}}"+
      "</td></tr><tr><th>Gender: </th> <td> {{gender}}"+
      "</td></tr><tr><th>City: </th> <td> {{city}}"+
      "</td></tr><tr><th>Country: </th><td>"+
      "{{country}} </td></tr></table>");
    view2 = view({email: info["data"].email,
  firstname: info["data"].firstname,
  lastname: info["data"].familyname,
  gender: info["data"].sex,
  city: info["data"].city,
  country:  info["data"].country
  });
    console.log(view2);
    return view2;
}


functionsignup = function(){
  var pass1 = document.getElementById("passwordsignup").value;
  var pass2 = document.getElementById("repeatpsw").value;

  console.log(pass1);
  console.log(pass2);
  if (pass1 === pass2) {
    //localhost?
    //socket.send(1);

    var login_object = {
      "email":document.forms["signupform"]["emailsignup"].value,
      "password":document.forms["signupform"]["passwordsignup"].value,
      "firstname":document.forms["signupform"]["firstname"].value,
      "familyname":document.forms["signupform"]["familyname"].value,
      "sex":document.forms["signupform"]["gender"].value,
      "city":document.forms["signupform"]["city"].value,
      "country":document.forms["signupform"]["country"].value
    };

    var message;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        message = JSON.parse(xhttp.responseText);
        console.log(message["Success"]);
        if(message["Success"]){
          //conSocketReg();
        }
        document.getElementById("signuperror").innerHTML = message["Message"];
      }
    };
    xhttp.open("POST", "/signup", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(login_object));

    //var message = serverstub.signUp(login_object);

    //return message["success"];
  }else {
    document.getElementById("signuperror").innerHTML = "passwords don't match";
    return false;
  }
};

function createHash(userToken){
  hash =  CryptoJS.SHA512(userToken);
    return hash.toString();
}

functionsignin = function(){
  var email = document.getElementById("emailsignin").value;
  var params = email;
  params += document.getElementById("passwordsignin").value;
  var hash = (CryptoJS.SHA512(params)).toString();
  var login_object = {
    "email":document.getElementById("emailsignin").value,
    "password":document.getElementById("passwordsignin").value,
    "hash":hash
  };
  //console.log(user);
  //console.log(pass);

  var message;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      message = JSON.parse(xhttp.responseText);
      document.getElementById("signinerror").innerHTML = message["message"];
      document.getElementById("signinerror").innerHTML = message["message"];
      userEmail = email;
      localStorage.setItem("token", message["data"]);

      if (message["Success"]) {
          window.onload();
      }
    }
  };
  xhttp.open("POST", "/signin", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.send(JSON.stringify(login_object));

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

  var params = oldpass;
  params += pass1;
  params += localStorage.getItem("token");
  var hash = (CryptoJS.SHA512(params)).toString();

  console.log(pass1);
  console.log(pass2);
  if (pass1 === pass2) {
    if(oldpass != pass1){

      var send_object = {
        //"token":localStorage.getItem("token"),
        "email":userEmail,
        "oldpassword":oldpass,
        "newpassword":pass1,
        "hash":hash
      };
      var message;
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          message = JSON.parse(xhttp.responseText);
          document.getElementById("changepswerr").innerHTML = message["message"];

        }
      };
      xhttp.open("POST", "/changepass", true);
      xhttp.setRequestHeader("Content-Type", "application/json");
      xhttp.send(JSON.stringify(send_object));


      //var message = serverstub.changePassword(localStorage.getItem("token"), oldpass, pass1);

    }else{
      document.getElementById("changepswerr").innerHTML = "password can't be the same as the old";
    }

  }else {
    document.getElementById("changepswerr").innerHTML = "new password don't match!";
  }

    //document.getElementById("changepswerr").innerHTML = "error here";
}


functionlogout = function(){
  socket.close();



  var send_object = {
    "token":localStorage.getItem("token")
  };
  var message;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      message = JSON.parse(xhttp.responseText);

    }
    localStorage.removeItem("token");
  };
  xhttp.open("POST", "/signout", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.send(JSON.stringify(send_object));

  view = document.getElementById("welcomeview").innerHTML;
  document.getElementById("content").innerHTML = view;
}



functionuploadmes = function(){
  var text = document.getElementById("submittext").value;
  console.log(text);
  document.getElementById("submittext").value = "";
  insertText(text, "thewall");

  var params = localStorage.getItem("token");
  params += text;
  params += localStorage.getItem("email");
  var hash = (CryptoJS.SHA512(params)).toString();

  var send_object = {
    "token":localStorage.getItem("token"),
    "messages":text,
    "receiver":localStorage.getItem("email"),
    "hash":hash
  };
  var message;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      message = JSON.parse(xhttp.responseText);

    }
  };
  xhttp.open("POST", "/postmessage", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.send(JSON.stringify(send_object));


  //serverstub.postMessage(localStorage.getItem("token"), text, email)


}

functionReloadMessage = function()
{

  //console.log("Testing functionReloadMessage")
  var chatArea = document.getElementById("thewall");
  chatArea.innerHTML = " ";
  var data;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      data = JSON.parse(xhttp.responseText);
      var messages = data["data"];

      console.log(messages);
      insertText(messages, "thewall");
    }
  };
  xhttp.open("GET", "/messagebytoken", true);
  xhttp.setRequestHeader("token", localStorage.getItem("token"));
  xhttp.send();



  //var receivedText = serverstub.getUserMessagesByToken(localStorage.getItem("token"));
  /*var messages = data["data"];
  var chatArea = document.getElementById("thewall");
  chatArea.innerHTML = "";
  insertText(messages, "thewall");
  var messageArray = data["data"];
  var chatArea = document.getElementById("thewall");
  chatArea.innerHTML = "";
  var i = messageArray.length -1;

  for (i; i >= 0; i--) {
  //  console.log(messageArray[i].writer);
    //console.log(messageArray[i].content);
    insertText(messageArray[i].writer, messageArray[i].content, "thewall");
  }*/

}

functionReloadMessageOther = function()
{


  var data;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      data = JSON.parse(xhttp.responseText);
      var messages = data["data"];
      var m = document.getElementById("m").innerHTML;
      var cM = Handlebars.compile("m");
      document.getElementById("allmessages").innerHTML = cM({messages: message});

      var chatArea = document.getElementById("thewallOther");
      chatArea.innerHTML = "";
      insertText(messages, "thewallOther");
    }
  };
  xhttp.open("GET", "/messagebyemail", true);
  xhttp.setRequestHeader("token", localStorage.getItem("token"));
  xhttp.setRequestHeader("email", localStorage.getItem("browse"));
  xhttp.send();


  //console.log("Testing functionReloadMessage")
  //var receivedText = serverstub.getUserMessagesByEmail(localStorage.getItem("token"),localStorage.getItem("browse"));


  /*var messageArray = receivedText["data"];
  var chatArea = document.getElementById("thewallOther");
  chatArea.innerHTML = "";
  var i = messageArray.length -1;
  for (i; i >= 0; i--) {
  //  console.log(messageArray[i].writer);
    //console.log(messageArray[i].content);
    insertText(messageArray[i].writer, messageArray[i].content, "thewallOther");
  }*/

}

insertText = function(text, wall)
{
 var elem = document.getElementById(wall);
 elem.innerHTML += text + '\n';

}

functionBrowseUser = function()
{
  var email = document.getElementById("searchUser").value;
  //localStorage.removeItem("browse");
  localStorage.setItem("browse", email);


  var info;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      info = JSON.parse(xhttp.responseText);
      console.log(info["Success"])
      if (info["Success"]) {
        //document.body.appendChild(document.getElementById("submitSearch"));
        //profileInfo(info)
        document.getElementById("browseArea").innerHTML = document.getElementById("browseProfile").innerHTML;
        document.getElementById("information").innerHTML = profileInfo(info);
      }else {
        //error message
        document.getElementById("searchError").innerHTML = info["message"];
        console.log(info["message"]);
      }
    }
  };
  xhttp.open("GET", "/databyemail", true);
  xhttp.setRequestHeader("token", localStorage.getItem("token"));
  xhttp.setRequestHeader("email", email);
  xhttp.send();



  //info = serverstub.getUserDataByEmail(localStorage.getItem("token"), email);

  console.log("Testing functionBrowseUser");
  console.log(document.getElementById("searchUser").value);
}

sendMessageToEmail = function(){
  var text = document.getElementById("submittexttouser").value;
  document.getElementById("submittexttouser").value = "";
  console.log(text);
  var email = localStorage.getItem("browse");
  console.log(email);

  var params = localStorage.getItem("token");
  params += text;
  params += localStorage.getItem("email");
  var hash = (CryptoJS.SHA512(params)).toString();


  var send_object = {
    "token":localStorage.getItem("token"),
    "messages":text,
    "receiver":email,
    "hash":hash
  };

  var message;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      message = JSON.parse(xhttp.responseText);

    }
  };
  xhttp.open("POST", "/postmessage", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.send(JSON.stringify(send_object));



  //serverstub.postMessage(localStorage.getItem("token"), text, email)
  insertText(text, "thewallOther");


}

var socket;
var chartUsers;
var chartUsersGender

conSocket = function(email){
  socket = new WebSocket("ws://" + document.domain + ":5001/socket");
  var data = {
    "email":email
  };
  console.log(email);


  socket.onopen = function(){
    socket.send(JSON.stringify(data));
  }


  socket.onmessage = function(msg){
    data = JSON.parse(msg.data);
    if(data["success"] == true && data["updateloggedin"] == false){
      functionlogout();
    }else{
      updateChart(data["online"], data["offline"],chartUsers);
      updateChart(data["male"], data["female"],chartUsersGender);

    }
  }

  socket.onclose = function(){
    console.log("closed socket connection");
    functionlogout();
  }

  socket.onerror = function(){
    socket.close();
    console.log("error with socket");

  }


}


conSocketReg = function(){
  socket = new WebSocket("ws://" + document.domain + ":5001/regsocket");
  var data = {
    "success": true
  };

  socket.onopen = function(){
    console.log("sending");
    socket.send(JSON.stringify(data));
  }


  socket.onmessage = function(msg){
    data = JSON.parse(msg.data);
  }

  socket.onclose = function(){
    socket.close();
    console.log("closed socket connection");
  }

  socket.onerror = function(){
    socket.close();
    console.log("error with socket");

  }


}







initChart = function(data1, data2, label1, label2, id, headerText){
  return new Chart(document.getElementById(id), {
      type: 'doughnut',
      data: {
        labels: [label1, label2],
        datasets: [
          {
            label: "users",
            backgroundColor: ["blue", "red"],
            data: [data1, data2]
          }
        ]
      },
      options: {
        title: {
          display: true,
          text: headerText
        }
      }
  });
}

updateChart = function(online, offline, chart){
  console.log(offline);
  if (offline == -1){
    chart.data.datasets[0].data[0] = online;
    chart.update();
  }else if (online == -1){
    chart.data.datasets[0].data[1] = offline;
    chart.update();
  }else{
    chart.data.datasets[0].data[0] = online;
    chart.data.datasets[0].data[1] = offline;
    chart.update();
  }

}
