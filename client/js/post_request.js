'use strict';
let crypto;
try {
  crypto = require('crypto');
} catch (err) {
  console.log('crypto support is not available!');
}
const $ = require('jQuery');
const bcrypt = require('bcrypt');

var hashAndSalt = function(password) {
    let salt = '$2b$12$RhUW67z9C.vlzlIU3ED68O';
    let password_hash = bcrypt.hashSync(password, salt);
    console.log(btoa(password_hash));
    return btoa(password_hash);
}

// doesn't work since the initial response from the server doesn't work
// This function validates the user's token is valid.
function validateUser(response){
    //doesn't actually work yet since I can't see response from server
    //data = response.token
    //temp value
    Data = {"token": "CPKGkXpK2NR6iURZ7joX8toySsnWGLufmUZdKLSoiqkvipW0NtIv9bMlI-4ibfacm0_yzJHW1nv134d5RQMd00uXbR_svA2Jgu8VQSwvU3c5f-38fZZoYyrt4OWwc6SmBB9VA8laC_RJ1HGhQD1MYolm9i54gcmzFHYBBoBrpCU"}
    $.ajax({
        url: 'http:localhost:8080/users/validate',
        type: "POST",
        data: Data,
        success: function(result){
            //for now return true
            // should the response `valid` be true then return true
            if(result.valid){
                return true;
            }
            else{
                return false;
            }
        },
        error: function(error) {
            console.log(`Error ${error}`)
        }

    })
}
const Url = 'http:localhost:8080/login'; 

// When the submit button in the login.html form
// is clicked, this function is activated
$('#btn').click(function() {
    event.preventDefault();
    const data = {
        username: $('#username').val(),
        password: hashAndSalt($('#password').val())
    };
    console.log(data)
    $.ajax({
        url: Url, 
        type: "POST",
        data: data,
        success: function(result) {
            // On success should return user id and user token which can be used to identify user
            console.log(result)
            // successful token validation, go to page
            if(validateUser(result)){
                window.location.href = "index.html"
            } 
            else{
                //consuming error -- eventually we want to let the user know they typed the wrong username/password
            }
        },
        error: function(error) {
            console.log(`Error ${error}`)
        }
    });
});