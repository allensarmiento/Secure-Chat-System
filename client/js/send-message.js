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
var messageFloor = 0;
function incMessageFloor(){ this.messageFloor++;}
function getMessageFloor(){ return this.messageFloor; }

// Executes when the user clicks the send button.
$('#send-btn').click(function() {
    event.preventDefault();
    checkUserName().done(function(result){prepareMessage(result)});
});

// Executes when the user hits the enter button.
document.onkeypress = keyPress;
function keyPress(e) {
    var x = e || window.event;
    var key = (x.keyCode || x.which);
    if (key === 13 || key === 3) 
        checkUserName().done(function(result){prepareMessage(result)});
}

//============= PREP AND SIGN MESSAGING STUFFS =============
// Prepares the message for ajax request.
// NOTE: Not sure if the token should be the sender or the recipient.
function prepareMessage(user) {
    var privateKey = fs.readFileSync(`../user_private_key_${user.name.slice(-1)}.pem`, "utf-8");

    let message = document.getElementById("message").value;
    var data = {
        token: window.localStorage.getItem("token"), // username
        channel_id: window.localStorage.getItem("chat_session_id"),
        signature_method: getSignatureValue(), // method of signature used
        signature: signMsg(message, privateKey), // sign message (should be one way hash)
        message: encryptMessage(message, window.localStorage.getItem("symkey")) // encrypt message
    };
    console.log(data.signature);
    data.signature = data.signature.toString('base64')
    // Viewing the data being sent in the console for debugging purposes
    // Call the send message function and verify the message has been send.
    sendMessage(data).done(function(data) {
        if (data) 
            console.log("Message sent");
    });
}

// Sending the message to server with ajax
function sendMessage(data) {
    return $.ajax({
        url: 'http:localhost:8080/chat/send',
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
        if (signatureType[i].checked) { return signatureType[i].value; }
    }
    return null;
}

// Signs a message sent by a user and returns the signature.
function signMsg(message, privateKey) {
    // Determine if using rsa, dsa, or none was selected.
    let signType = getSignatureValue();
    let sign;
    if (signType === 'rsa') { sign = crypto.createSign('RSA-SHA256'); }
    else if (signType === 'dsa') { sign = crypto.createSign('DSA-SHA256'); }
    sign.update(message);
    sign.end();

    return sign.sign(privateKey);
}

// Verifies that the signature matches the message
// NOTE: THERE IS SOMETHING WRONG WITH THE WAY I'M DECODING FROM THE SERVER
function verifyMsg(signature, publicKey, signature_method) {
    var uint8View = new Uint8Array(signature);
    console.log(uint8View)
    // NOTE: RSA-SHA256 or DSA-SHA256 may need to be passed in instead, but haven't been able to test the signMsg first.
    const verify = crypto.createVerify(signature_method);
    verify.update(uint8View);
    verify.end();
    return verify.verify(publicKey, uint8View);
}


//=========== CHECK ONLINE USERS STUFFS===============
// Sets the user to online status
function setActiveUser(username) {
    document.getElementById(username).setAttribute("class", "activeUser");
}

// Sets the user to offline status
function setInactiveUser(username) {
    document.getElementById(username).setAttribute("class", "inactiveUser");
}


//============= ADDING USERS TO CHAT SESSIONS STUFF======
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

// Sends all the people added to the chat to the server to generate symkey
function startChatting() {
    if (chatters.size === 0) { alert("You didn't chose anyone to chat with!"); } 
    else {
        console.log(chatters);
        fetchSymmetricKey(Array.from(chatters)).done(function (result) {
            if (window.localStorage.getItem("symkey") !== undefined) { window.localStorage.removeItem("symkey"); }
            checkUserName().done(function(user){
                window.localStorage.setItem("symkey", decryptSymmetricKey(user.name.slice(-1), result[result.length-1].symmetric_key))
                window.localStorage.setItem("chat_session_id", result[result.length-1].chat_session_id)
            });
        });
    }
}

// Adds the selected users to a channel to initiate the symmkey
//  returns chat_session_id and symm key
function fetchSymmetricKey(chatters) {
    var data = {
            'token':window.localStorage.getItem("token"),
            'usernames': chatters
            };
    return $.ajax({
        url: 'http://localhost:8080/chat/initiate',
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

// takes the user's id / number form the users name ex: Name1
// and a key to be decrypted by our secret key
function decryptSymmetricKey(user, symkey) {
    var privateKey = fs.readFileSync(`../user_private_key_${user}.pem`, "utf8");
    var buffer = Buffer.from(symkey, "base64");
    var decrypted = crypto.privateDecrypt(privateKey, buffer);
    return decrypted.toString("utf8");
}


// on load, check who is online
window.onload = function() {
    loadOnlineStatus();
}

function getPublicKey(token, user){
    var data = {
        'token':token,
        'user_name':user
    }
    return $.ajax({
        url: 'http://localhost:8080/users/public_key', 
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        success: function(result) {
           return result
        },
        error: function(error) {
            console.log(`Error ${JSON.stringify(error)}`);
        }
    });
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

// checks online status of the user using their username
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

// grabbing the name of the current user that owns the session id
function checkUserName(){
    var data = {'token': window.localStorage.getItem("token")}
    return $.ajax({
        url: 'http://localhost:8080/users/name',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        success: function(result) {
            console.log(result)
            return result;
        },
        error: function(error) {
            console.log(`Error $({JSON.stringify(error)}`);
        }
    });
}

// Takes the user's local symmetric key and ecrypts the message after signature
function encryptMessage(signedMsg, symKey){
    var cipher = crypto.createCipher('aes-128-cbc', symKey)
    // cipher.setAutoPadding()
    var encrypted = cipher.update(signedMsg, 'utf8', 'base64')
    encrypted += cipher.final('base64')
    return encrypted
}

// decrypts the message from the server using the symmetric key
// NOTE: think we use base64 encoding on return? not sure.
function decryptMessage(encMsg, symKey){
    var decipher = crypto.createDecipher('aes-128-cbc', symKey)
    var decrypted = decipher.update(encMsg, 'base64', 'base64')
    decrypted += decipher.final('base64')
    return atob(decrypted)
}

// going through the methos to decrypt the message from the server
// takes in an encrypted message

//update the chatbox with new messages from the server
// expects an array from the server, will be empty if nothing has updated
// NOTE: replace rsa-sha256 with signature_method
function updateChatBox(response){
    for (var i = 0; i < response.messages.length; ++i){
        var message = response.messages[i].message;
        var signature = response.messages[i].signature;
        var signMethod = response.messages[i].signature_method;
        var name = response.messages[i].user_name;
        console.log("after database ", signature)
        if(signMethod == 'rsa'){
            signMethod = 'RSA-SHA256'
        }
        getPublicKey(window.localStorage.getItem("token"), name).done(function(result){
            if(verifyMsg(_base64ToArrayBuffer(signature), atob(result.public_key), signMethod)){
                response.message = decryptMessage(message, window.localStorage.getItem("symkey"))
            }
            else{
                console.log("decryptor invalid signature?")
            }
        })
            document.getElementById("message").value = "";
            document.getElementById("chatbox").innerHTML +=
              "<p class='chatmessage sent'>" + result.name + " : " + result.message + "</p>";
          
            let chatbox = document.getElementById("chatbox");
            chatbox.scrollTop = chatbox.scrollHeight;
            incMessageFloor();
    }
}

// Timer to poll the database for messages. polls every 3.5 seconds.
setInterval(
    function()
    {
        var floorValue = getMessageFloor()
        var data = {
            'token': window.localStorage.getItem("token"),
            'channel_id': window.localStorage.getItem("chat_session_id"),
            'message_floor': floorValue.toString()
        }
        $.ajax({
            url: 'http://localhost:8080/chat/messages',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function(result) {
                updateChatBox(result)
            },
            error: function(error) {
                console.log(`Error $({JSON.stringify(error)}`);
            }
        });
    }, 
    5000
)

function _base64ToArrayBuffer(base64) {
    var binary_string =  window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array( len );
    for (var i = 0; i < len; i++)        {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}