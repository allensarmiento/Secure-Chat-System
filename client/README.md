# Client

## How to execute:
```
npm install
npm start
```

## send-message.js Notes
User variable undefined for this call:<br>
```
var relativePath = path.relative(`../../user_private_key_${user.slice(-1)}.pem`);
```

Calling this has an error, assuming it doesn't like the path
```
var relativePath = path.relative(`../../user_private_key_1.pem`);
```

Don't think DSA-SHA256 is included in the crypto library, so may need to be imported.  
