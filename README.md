# Test Game

API Manage hotels and rooms

## Getting Started

To have a copy of the repository on your machine we must clone the repository

* Clone repository
```ssh
    git clone git@github.com:pollitosabroson/test_crm.git
```

### Prerequisites

Make sure that you have met the following prerequisites before continuing with this tutorial.

* Logged in as a user with sudo privileges or Admin user for MAC.
* Have [Docker](https://docs.docker.com/install/) installed

### Installing 

To install the project, we must access the docker folder, after the environment we are going to execute, in this case it is the one of dev and we execute the following commands.

* access folder
```ssh
  cd test_crm/docker/dev
```
* Create dockers
```ssh
  docker-compose build --no-cache --force-rm
```
* Run dockers
```ssh
  docker-compose up -d
```
* Apply migrations
```ssh
  docker exec -it dev_roiback_api_1 python manage.py migrate
```

* Access

    * API: [localhost:8091](http://localhost:8091/)

## Running the tests

To run the tests just execute them via docker exec
* API
```ssh
  docker exec -it dev_roiback_api_1 pytest -v
```

## Enviroments
Show all folders that are divided by environment
* DEV
    * docker/dev

* QA
    * docker/qa

* PROD
    * docker/PROD
