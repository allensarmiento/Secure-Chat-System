//TODO: at some point remove all console.log statements

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

const Url = 'http:localhost:8080/login'; 

// When the submit button in the login.html form
// is clicked, this function is activated
$('#btn').click(function() {
    event.preventDefault();
    const data = {
        'username': $('#username').val(),
        'password': hashAndSalt($('#password').val())
    };
  
    // since web requests are asynchronous we need to make promises
    loginUser(data).done(function(data){
        window.localStorage.setItem("token", data.token)
        window.localStorage.setItem("chat_id", data.id)
        if(data){
            window.location.href = "index.html"
        }
    })
});



function loginUser(data){
    return $.ajax({
         url: Url, 
         contentType: 'application/json',
         type: 'POST',
         data: JSON.stringify(data),
         success: function(result) {
             validateUser(result).done(function(data){
                 return true;
             });
         },
         error: function(error) {
             console.log(`Error ${error}`)
         }
     })
 }
 

function validateUser(response){
    console.log(response.token)
    var data = {'token':response.token}
    return $.ajax({
        url: 'http:localhost:8080/users/validate',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        success: function(result){
            if(result.valid){
                return true;
            }
            else{
                return false;
            }
        },
        error: function(error) {
            console.log(`Error ${error}`)
            return false;
        }

    })
}
