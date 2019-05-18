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

/**
 * @return signatureType - Returns either rsa or dsa
 */
function getSignatureValue() {
    var signatureType = document.getElementsByName('signature');

    for (let i = 0; i < signatureType.length; i++) {
        if (signatureType[i].checked) {
            return signatureType[i].value;
        }
    }
    return null;
}

/**
 * @param {string} message - Message typed in input field
 * @return signature
 */
function signMsg(message, privateKey) {
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
    const signature = sign.sign(privateKey);
    
    return signature;
}

/**
 * @param {string} message - Message typed in input field
 * @param publicKey - public key
 * @param signature - signature
 */
function verifyMsg(message, publicKey, signature) {
    const verify = crypto.createVerify('SHA256');
    verify.update(message);
    verify.end();
    return verify.verify(publicKey, signature);
}

// Executes when the user clicks the send button
$('#send-btn').click(function() {
    event.preventDefault();

    // Obtain the private key
    // NOTE: Error occurs on the user
    var relativePath = path.relative(`../../user_private_key_${user.slice(-1)}.pem`);
    var privateKey = fs.readFileSync(relativePath, "utf8");

    // Data is pass in:
    //  - token = username
    //  - message = message the user entered
    //  - signature = signature returned from signMsg function
    let message = document.getElementById("message").value;
    const data = {
        token: window.localStorage.getItem("token"),
        message: message,
        signature: signMsg(message, privateKey) // NOTE: Need a way to get the private key
    };
    // Viewing the data being sent in the console for debugging purposes
    console.log(data);

    // Verify the message has been sent
    sendMessage(data).done(function(data) {
        if (data) {
            console.log("Message sent");
        }
    });
});

function sendMessage(data) {
    return $.ajax({
        url: 'http:localhost:8080/users/send',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        success: function(result) {
            if (result.valid) {
                return true;
            } 
            else {
                return false;
            }
        },
        error: function(error) {
            console.log(`Error ${error}`);
            return false;
        }
    });
}

// Alternative way of sending a message by hitting the enter key
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
        setInactiveUser(result.name);
        alert("USER : " + result.name + " is offline!")
    }
  })

  // for every addChatter, show list of who's going to be chatting to user.
}

// TODO: store the symmetric key then begin chatting
function startChatting(){
    if (chatters.size == 0){
        alert("You didn't choose anyone to chat with!")
    }
    else{
        console.log(chatters);
        fetchSymmetricKey(Array.from(chatters)).done(function (result) {
            if (window.localStorage.getItem("symkey") != undefined){
            window.localStorage.removeItem("symkey")
        }
            window.localStorage.setItem("symkey") = decryptSymmetricKey(result)
            console.log( window.localStorage.getItem("symkey"))
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