# Pastebin app with DRF (Django REST framework)

### Overview
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
- **for Docker configuration you must have Docker and Docker Compose installed on your labtop**
- **for testing API endpoint you will need disktop application `Postman` or similar application**

### Before run application

- create file in path `config` with name `app.env` and add variables to this file:

  - `SECRET` put on this variable django app secret key
  - `DEBUGGER` put on this variable boolan flag reflect debugger mode in django app with python format (eg. `False`)
  - `HOSTS` put on this variable string contain all allwed hosts separated by `,`
  - `DB_NAME` put on this variablestring database name
  - `DB_USER` put on this variablestring database user role
  - `DB_PASSWORD` put on this variablestring database password
  - `DB_HOST` put on this variablestring docker compose database service name
  - `DB_PORT` put on this variablestring database port `5432`

- create file in path `config` with name `db.env` and add variables to this file:

  - `POSTGRES_DB` put on this variablestring database name
  - `POSTGRES_USER` put on this variablestring database user role
  - `POSTGRES_PASSWORD` put on this variablestring database password

- example on variable `DEBUGGER=False`

- to test all API endpoint you will find `Pastebin.collection.json` file on the root of repository you can import this file on `Postman` to get application collection

- you can allows change collection variables

## Lunch project with Docker

- make sure you are on root path of repository
- build docker containers by run this commans `docker-compose build`
- create migrations file by run `docker-compose run web src/manage.py makemigrations`
- migrate project model by run `docker-compose run web src/manage.py migrate`
- create project super user `docker-compose run web src/manage.py createsuperuser`
- collect static files `docker-compose run web src/manage.py collectstatic --no-input`
- startup project `docker-compose up`
- you can open project url [localhost](http://localhost/) or [localhost](http://127.0.0.1/)
- you can use `Postman` to test all API endpoint


## Lunch project with Pipenv
- create `.env` file and pass all data like `config/app.env` from previous docker section
- run `pipenv shell` to create virtual environment
- run commend `pipenv install` to install dependency package
- make sure you have PostgreSql database with credential provided on `.env` file
- run command `python src/manage.py makemigrations`
- run command `python src/manage.py migrate`
- run command `python src/manage.py createsuperuser`
- run command `python src/manage.py runserver`
- you can open project url [localhost](http://localhost:8000/) or [localhost](http://127.0.0.1:8000/)
- you can use `Postman` to test all API endpoint

---
**Thanks and i hope my skills on this task match with your requirements**