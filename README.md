# Secure-Chat-System

## Group Members
  * Nathan S
  * Stephen S
  * Jasper C
  * Allen S
  * Hector M

## Contributions of each member
  * Front-End: Allen, Hector
  * Back-End: Nathan, Stephen, Jasper

## How to Execute (Client)
```
cd client
npm install  
npm start  
```

##### In case you get NODE_MODULE_VERSION errors for bcrypt

```
npm install --save-dev electron-rebuild

# Every time you run "npm install", run this:
./node_modules/.bin/electron-rebuild
```

## How to Execute (Server)
```
cd server
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd ..
python3 server/ChatServer
```

## Description
This project implements a secure chat system where one or more users can join together in a group chat. Each user must be registered with the chat server through a username and password. Security is established through the use of a symmetric key between all users within the chat.

## Programming Languages/Tools:
**Electron (HTML, CSS, JavaScript, jQuery):** We chose to use Electron because it is a technology that is used to build desktop applications and we create our secure chat application with HTML, CSS, JavaScript, and jQuery. This is the front-end portion of the project. Some of the modules we needed to import include: jQuery to handle ajax requests, crypto for creating digital signatures, and bcrypt to hash and salt passwords.<br><br>
**Python:** For the back-end portion of the project, we chose to use Python because it was the most preferred language among the members of the group. We decided it would be best to use this language because everyone has experience working coding in Python.<br><br>
**Postman:** This is a tool we utilized to figure out the start and end points for communicaiton between the client and server. Using this tool, we could get an idea of what our expected results and flow of the application should be.<br>

## Configuration/Set up:
For the client side, the set up was to start a basic Electron app and progress from there. Once we began importing modules for node.js, we ran into issues. One problem we encountered is that some modules are not up to date with our current version of Electron, so we had to make sure that we everything we are using are the latest versions that are compabitble with one another. We ran into an issue where bcrypt wasn't working because the module was not being read as compatible. The issue was fixed through executing a command after installing all the node modules.<br><br>
For the server side, the set up was getting the database up and running as well as making sure communication is established between client and server. We also needed to make sure that everyone is using the same version of python.

## Challenges and Solutions:
We encountered a lot of challenges in this project. The biggest challenge would be not fully understanding the task and process of creating a secure chat application. We solved this by communicating our thoughts and ideas and worked together to come upon an agreement. Another challenge we faced is understanding how to call different functions within the modules we imported. We had a problem with the verification of the digital signature always returning false, and we found the issue was what we passed into the parameter. Some function parameters are different between languages, in our case JavaScript and Python. We were able to find a solution by looking through the code and reading up on the functions we were utilizing.

