// already declared in send-message.js
// const $ = require('jQuery');

const Url = 'http:localhost:8080/users/logout';

$('#logout-btn').click(function() {
    event.preventDefault();
    const data = {
        token: window.localStorage.getItem("token")
    };
    logoutUser(data).done(function(data) {
        if (data) {
            window.location.href = "login.html";
        }
    });
});

function logoutUser(data) {
    return $.ajax({
        url: Url,
        contentType: 'application/json',
        type: 'DELETE',
        data: JSON.stringify(data),
        success: function(result) {
            console.log(result);
            validateUser(result).done(function(data){
                console.log(data);
                return true;
            });
        },
        error: function(error) {
            console.log(`Error ${error}`);
        }
    });
}

function validateUser(response){
    console.log(response.token);
    var data = {'token':response.token};
    return $.ajax({
        url: 'http:localhost:8080/users/validate',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(data),
        success: function(result){
            console.log(result.valid);
            if(result.valid){
                return true;
            }
            else{
                return false;
            }
        },
        error: function(error) {
            console.log(`Error ${error}`);
            return false;
        }

    });
}