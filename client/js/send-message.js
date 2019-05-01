function sendMessage() {
  let message = document.getElementById("message").value;
  document.getElementById("message").value = "";

  document.getElementById("chatbox").innerHTML +=
    "<p class='chatmessage sent'>" + message + "</p>";

  let chatbox = document.getElementById("chatbox");
  chatbox.scrollTop = chatbox.scrollHeight;
}

document.onkeypress = keyPress;

function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    sendMessage();
  }
}

function setActiveUser(username) {
  document.getElementById(username).appendChild(document.createElement("p")).setAttribute("class", "activeUser");
  document.getElementById(username).querySelector("p").innerText = "✓";
}

function setInactiveUser(username) {
  document.getElementById(username).appendChild(document.createElement("p")).setAttribute("class", "inactiveUser");
  document.getElementById(username).querySelector("p").innerText = "x";
}

// testing activation of users for login/logout
setActiveUser("allen");
setInactiveUser("hector");
setInactiveUser("nathan");
setActiveUser("stephen");
setInactiveUser("jasper");
