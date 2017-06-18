# our base image
FROM alpine:3.5

# Install python and pip
RUN apk add --update py2-pip

# upgrade pip
RUN pip install --upgrade pip

# make work directory
RUN mkdir /usr/data /usr/tmp
WORKDIR /usr/tmp

# install Python modules needed by the Python app
COPY requirements.txt /usr/tmp/
RUN pip install --no-cache-dir -r /usr/tmp/requirements.txt

VOLUME /usr/app

# tell the port number the container should expose
EXPOSE 5000
