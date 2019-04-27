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

## Programming Languages/Tools:
  * Electron

## How to Execute
Clone this repository ane make sure to have Node.js installed. Execute the following:  
    npm install  
    npm start  

## Description (To be deleted before submission):
Implementation of a system which enables a group of users to chat securely.  
All users are registered with the chat server. When the user wants to chat with  
another registered user, he first connects to the chat server and enters his/her  
user name and password. The server verifies the user name and password, and if  
correct, the user's status is changed to "online". Next, the user may enter  
the user ids of users with whom he wishes to chat (could be more than one). At  
any given time the user should be able to check what other users are online and  
invite them to the ongoing conversation.  

Once the user specifies the users with whom he wishes to chat, the server  
generates a symmetric key, and securely distributes it to all the specified users  
and the user who initiated the chat. To achieve secure key distribution you must  
encrypt the symmetric key using the public keys of the respective users (you may  
assume that server knows the public keys of all users). If one of the specified  
users is not online, the requesting user is notified about this.  

After the encrypted symmetric key has been distributed to all users, the users  
decrypt the symmetric key using their private keys, and the chat session may  
begin. All messages exchanged during the chat must be encrypted using the  
symmetric key provided by the server and must be delivered to all users  
participating in the chat. Any user may choose to leave the conversation. If  
the user disconnects from the chat server, his status should be changed to  
"offline". All users who are connected to the server, must have a way to check  
whether a given user is online.  

Multiple chat sessions does not need to be supported.  

Implementation must provide both confidentiality and digital signature. For  
digital signature, provide the user with a choice of using RSA or Digital  
Signature Algorithm (DSA; https://bit.ly/2TvvGst). Both digital signature  
schemed must be supported.  

