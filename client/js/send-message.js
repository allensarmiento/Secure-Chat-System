function sendMessage() {
  let message = document.getElementById("message").value;
  document.getElementById("message").value = "";

  document.getElementById("messages").innerHTML += 
    "<p>" + message + "</p>";
}

