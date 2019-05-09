'use strict';
let crypto;
try {
  crypto = require('crypto');
} catch (err) {
  console.log('crypto support is not available!');
}
const $ = require('jQuery');
const bcrypt = require('bcrypt');
// var hash = bcrypt.hashSync(myPlaintextPassword, salt);
// hashAndSalt
// Takes in a password and a salt to generate the new password
// The hashing algorithm is sha512 and the salt is a string
var hashAndSalt = function(password) {
    let salt = '$2b$12$RhUW67z9C.vlzlIU3ED68O';
    // let hash = crypto.createHmac('sha512', salt);
    // hash.update(password);
    // let password_hash = hash.digest('hex');
    let password_hash = bcrypt.hashSync(password, salt);
    console.log(password_hash);
    return password_hash;
}

// NOTE: To be added
// URL to send the POST data to,
// This should be the endpoint.
const Url = 'http:localhost:8080/login'; 

// When the submit button in the login.html form
// is clicked, this function is activated
$('#btn').click(function() {
    event.preventDefault();
    const data = {
        username: $('#username').val(),
        password: hashAndSalt($('#password').val())
    };
    console.log("data")
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

// const request = net.request({
//     method: 'GET',
//     protocol: 'http:',
//     hostname: 'localhost',
//     port: 8080,
//     path: '/login'
// })

// request.on('login', (authInfo, callback) => {
//     callback()
//   })