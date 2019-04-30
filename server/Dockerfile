FROM python:3-slim
LABEL maintainer="nathan@nathan-s.com"
RUN apt-get update && apt-get install -y \
 git \
 build-essential \
 zip \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /ChatApp
RUN git clone https://github.com/allensarmiento/Secure-Chat-System.git
RUN pip3 install wheel
RUN pip3 install setuptools
WORKDIR /ChatApp/Secure-Chat-System/server
RUN pip3 install --upgrade -r requirements.txt
WORKDIR /app
ENTRYPOINT ["python3", "/ChatApp/Secure-Chat-System/server/ChatServer"]