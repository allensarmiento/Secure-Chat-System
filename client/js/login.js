var form = document.getElementById("login-form");

form.addEventListener("submit", function(event){
    event.preventDefault();
    //make ajax call here

    //for now make it default to valid
    window.location.assign("index.html");
});

