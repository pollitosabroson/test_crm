# use base python image with python 3.5
FROM python:3.6

# add requirements.txt to the image
ADD requirements.txt /app/requirements.txt

# set working directory to /app/
WORKDIR /app/

# Install gettext for translations
RUN  apt-get update && apt-get install -y gettext

# install python dependencies
RUN pip install -U -r requirements.txt

RUN django-admin startproject roiback

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser
