const $ = require('jQuery');
const crypto = require('crypto');
var path = require("path");
var fs = require("fs");

/*
function sendMessage() {
  let message = document.getElementById("message").value;
  document.getElementById("message").value = "";

  document.getElementById("chatbox").innerHTML +=
    "<p class='chatmessage sent'>" + message + "</p>";

  let chatbox = document.getElementById("chatbox");
  chatbox.scrollTop = chatbox.scrollHeight;
}
*/

// Executes when the user clicks the send button.
$('#send-btn').click(function() {
    event.preventDefault();
    prepareMessage();
});
// Executes when the user hits the enter button.
document.onkeypress = keyPress;
function keyPress(e) {
    var x = e || window.event;
    var key = (x.keyCode || x.which);
    if (key === 13 || key === 3) 
        prepareMessage();
}

// Prepares the message for ajax request.
// NOTE: Not sure if the token should be the sender or the recipient.
function prepareMessage() {
    // NOTE: Error occurs on the user call
    var relativePath = path.relative(`../../user_private_key_${user.slice(-1)}.pem`);
    var privateKey = fs.readFileSync(relativePath, "utf-8");

    let message = document.getElementById("message").value;
    const data = {
        token: window.localStorage.getItem("token"), // username
        message: message, // message
        signature: signMsg(message, privateKey) // sign message
    };
    // Viewing the data being sent in the console for debugging purposes
    console.log(data);

    // Call the send message function and verify the message has been send.
    sendMessage(data).done(function(data) {
        if (data) 
            console.log("Message sent");
    });
}

// Sending the message to server with ajax
function sendMessage(data) {
    return $.ajax({
        url: 'http:localhost:8080/users/chat',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        success: function(result) {
            if (result.valid) 
                return true;
            else 
                return false;
        },
        error: function(error) {
            console.log(`Error ${error}`);
            return false;
        }
    });
}

// Reads in the radio buttons named "signature" and returns the signature type, either rsa or dsa.
function getSignatureValue() {
    var signatureType = document.getElementsByName('signature');
    for (let i = 0; i < signatureType.length; i++) {
        if (signatureType[i].checked) {
            return signatureType[i].value;
        }
    }
    return null;
}

// Signs a message sent by a user and returns the signature.
function signMsg(message, privateKey) {
    // Determine if using rsa, dsa, or none was selected.
    let signType = getSignatureValue();

    let sign;
    if (signType === 'rsa') {
        sign = crypto.createSign('RSA-SHA256');
    } else if (signType === 'dsa') {
        // NOTE: Couldn't find DSA, so may have to look for a way to import it.
        sign = crypto.createSign('DSA-SHA256');
    }
    sign.update(message);
    sign.end();

    return sign.sign(privateKey);
}

// Verifies that the signature matches the messsage
function verifyMsg(message, publicKey, signature) {
    const verify = crypto.createVerify('SHA256');
    verify.update(message);
    verify.end();
    return verify.verify(publicKey, signature);
}

// Sets the user to online status
function setActiveUser(username) {
    document.getElementById(username).setAttribute("class", "activeUser");
}

// Sets the user to offline status
function setInactiveUser(username) {
    document.getElementById(username).setAttribute("class", "inactiveUser");
}

// Add users to a chat session
const chatters = new Set();
function addChatter(user) {
checkOnlineStatus(user).done(function(result) {
    console.log(result);
    if (result.result) {
        console.log("In addChatter: Added chatter", result.name);
        chatters.add(result.name);
    } else {
        setInactiveUser(result.name);
        alert("USER : " + result.name + " is offline!");
    }
});
}

// TODO: store the symmetric key then begin chatting
function startChatting() {
    if (chatters.size === 0) {
        alert("You didn't chose anyone to chat with!");
    } 
    else {
        console.log(chatters);
        fetchSymmetricKey(Array.from(chatters)).done(function (result) {
            if (window.localStorage.getItem("symkey") !== undefined) {
                window.localStorage.removeItem("symkey");
            }
        window.localStorage.setItem("symkey") = decryptSymmetricKey(result);
        console.log(window.localStorage.getItem("symkey"));
        });
    }
}

function fetchSymmetricKey(chatters) {
    var data = {'usernames': chatters};
    return $.ajax({
        url: 'http://localhost:8080/users/chat',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        success: function(result) {
            return result;
        },
        error: function(error) {
            console.log(`Error $({JSON.stringify(error)}`);
        }
    });
}

function decryptSymmetricKey(symkey) {
    var relativePath = path.relative(`../../user_private_key_${user.slice(-1)}.pem`);
    var privateKey = fs.readFileSync(relativePath, "utf8");
    var buffer = Buffer.from(symKey, "base64");
    var decrypted = crypto.privateDecrypt(privateKey, buffer);
    return decrypted.toString("utf8");
}

// on load, check who is online
window.onload = function() {
    loadOnlineStatus();
}

function loadOnlineStatus() {
    for (let i = 1; i <= 5; i++) {
        checkOnlineStatus(`Name${i}`).done(function(result) {
            if (result.result) 
                setActiveUser(result.name);
            else 
                setInactiveUser(result.name);
        });
    }
}

// checkOnlineStatus
function checkOnlineStatus(user) {
    var data = {'username': user};
    return $.ajax({
        url: 'http://localhost:8080/users/status', 
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        success: function(result) {
            if (result.status === 'online') {
                result.result = true;
                return result;
            } else {
                result.result = false;
                return result;
            }
        },
        error: function(error) {
            console.log(`Error ${JSON.stringify(error)}`);
        }
    });
}
