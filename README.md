# Pastrbin app with DRf (Django REST framework)

## Overview

to know about this app and his goals please read `DOCS.md` file

## Used Technology

i'm using in this app:

- Django framework
- Django REST framework
- PostgreSQL
- NGINX
- Gunicorn
- Docker

## Getting Started

### Prerequisites

- **clone GitHub repository**
- **you must have Docker and Docker Compose installed on your labtop**
- **for testing API endpoint you will need disktop application `Postman` or similar application**

### Before run application

- create file in path `config/app` with name `.env` and add variables to this file:

  - `SECRET` put on this variable django app secret key
  - `DEBUGGER` put on this variable boolan flag reflect debugger mode in django app with python format (eg. `False`)
  - `HOSTS` put on this variable string contain all allwed hosts separated by `,`
  - `DB_NAME` put on this variablestring database name
  - `DB_USER` put on this variablestring database user role
  - `DB_PASSWORD` put on this variablestring database password
  - `DB_HOST` put on this variablestring docker compose database service name
  - `DB_PORT` put on this variablestring database port `5432`

- create file in path `config/db` with name `.env` and add variables to this file:

  - `POSTGRES_DB` put on this variablestring database name
  - `POSTGRES_USER` put on this variablestring database user role
  - `POSTGRES_PASSWORD` put on this variablestring database password

- example on variable `DEBUGGER = False`

- to test all API endpoint you will find `Pastebin.collection.json` file on the root of repository you can import this file on `Postman` to get application collection

- you can allows change collection variables

## Lunch Docker

- make sure you are on root path of repository
- build docker containers by run this commans `docker-compose build`
- collect static files `docker-compose run web hello/manage.py collectstatic --no-input`
