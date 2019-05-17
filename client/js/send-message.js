const $ = require('jQuery');
const crypto = require('crypto');
var path = require("path");
var fs = require("fs");

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
  document.getElementById(username).setAttribute("class", "activeUser");
}

function setInactiveUser(username) {
  document.getElementById(username).setAttribute("class", "inactiveUser");
}

// checkOnlineStatus only expects the name of the user
function checkOnlineStatus(user){
    var data = {'username': user}
    return $.ajax({
      url: 'http://localhost:8080/users/status', 
      contentType: 'application/json',
      type: 'POST',
      data: JSON.stringify(data),
      dataType: 'json',
      success: function(result) {
          if (result.status == "online") {
            result.result = true
            return result
          }
          else {
            result.result = false
            return result
          }
      },
      error: function(error) {
          console.log(`Error ${JSON.stringify(error)}`)
      }
    })
}

function fetchSymmetricKey(chatters){
  var data = {'usernames': chatters}
  return $.ajax({
    url: 'http://localhost:8080/users/chat', 
    contentType: 'application/json',
    type: 'POST',
    data: JSON.stringify(data),
    dataType: 'json',
    success: function(result) {
        return result
    },
    error: function(error) {
        console.log(`Error ${JSON.stringify(error)}`)
    }
  })
}


const chatters = new Set();
function addChatter(user){
  checkOnlineStatus(user).done(function(result){
    console.log(result);
    if(result.result)
    {
      console.log("In addChatter: Added chatter", result.name)
      chatters.add(result.name)
    }
    else
    {
      //TODO: then let user know that person is offline explicitly..?
      setInactiveUser(result.name);
      alert("USER : " + result.name + " is offline!")
    }
  })

  // for every addChatter, show list of who's going to be chatting to user.
}

// TODO: store the symmetric key then begin chatting
function startChatting(){
  if (chatters.size == 0){
    //TODO: say there are no online chatters available
  }
  else{
    console.log(chatters);
    fetchSymmetricKey(Array.from(chatters)).done(function (result) {
      console.log(decryptSymmetricKey(result))
    })
  }
}

// We will grab the private key from our directory, and the symmetric key will be found by the user number
function decryptSymmetricKey(symKey){
  var relativePath = path.relative(`../../user_private_key_${user.slice(-1)}.pem`)
  var privateKey = fs.readFileSync(relativePath, "utf8")
  var buffer = Buffer.from(symKey, "base64")
  var decrypted = crypto.privateDecrypt(privateKey, buffer)
  return decrypted.toString("utf8")
}



// on load, we check who is online
function loadOnlineStatus(){
  for(var i = 1; i <= 5; i++){
    checkOnlineStatus(`Name${i}`).done(function(result){
      if (result.result)
        setActiveUser(result.name)
      else
        setInactiveUser(result.name)
    })
  }
}

window.onload = function(){
  loadOnlineStatus()
}