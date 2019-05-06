# Server Guide

## Running
```text
docker build https://raw.githubusercontent.com/allensarmiento/Secure-Chat-System/master/server/Dockerfile -t chatserver --no-cache
docker run --name chatServer -it --rm -p 8080:8080 -v ${PWD}:/app chatserver
```