'use strict';
let crypto;
try {
  crypto = require('crypto');
} catch (err) {
  console.log('crypto support is not available!');
}
var $ = require('jQuery');

// hashAndSalt
// Takes in a password and a salt to generate the new password
// The hashing algorithm is sha512 and the salt is a string
var hashAndSalt = function(password) {
    let salt = '$2b$12$RhUW67z9C.vlzlIU3ED68O';
    let hash = crypto.createHmac('sha512', salt);
    hash.update(password);
    let password_hash = hash.digest('hex');
    return password_hash;
}

// NOTE: To be added
// URL to send the POST data to,
// This should be the endpoint.
const Url = '/'; 

// When the submit button in the login.html form
// is clicked, this function is activated
$('#btn').click(function() {
    /* This is for debugging purposes only */
    alert(hashAndSalt($('#password').val()));

    const data = {
        username: $('#username').val(),
        password: hashAndSalt($('#password').val())
    };

    $.ajax({
        url: Url, 
        type: "POST",
        data: data,
        success: function(result) {
            console.log(result)
        },
        error: function(error) {
            console.log(`Error ${error}`)
        }
    });
});
