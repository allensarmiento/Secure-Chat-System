# Client

## How to execute:
```
npm install
npm start
```

## send-message.js
Functions implemented:
* getSignatureValue() - checks what value is selected for either rsa or dsa
* signMsg(message, privateKey) - Digital signature for a message using rsa or dsa
    * **Shortcomings:** DSA-SHA256 was not found in the module, so would need to find a way to add it. The sign function needs to obtain the private key in order to work; currently unsure how to get the user value to get the relativePath. 
* verifyMsg(message, publicKey, signature) - verifies a message
* sendMessage() - function for ajax call to data to the server including: username, message, and signature.
