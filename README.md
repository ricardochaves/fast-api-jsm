# Fast API

## Pre requisito

- Python
- Django (pip install django)

## Clone infra

```bash
git clone git@github.com:ricardochaves/fast-api-jsm.git
```

## Inicio

Iniciando um projeto Django

```bash
docker-compose run --rm app django-admin startproject fast_api .
```

Executando

```bash
docker-compose up app
```

- http://0.0.0.0:8000/

Criando uma aplicação

```bash
docker-compose run --rm app python manage.py startapp core
```

-----> open -na "PyCharm.app" .

-----> Confirgurar interpretador

Enquanto ele fazer o build e o interpretador vamos criando as classes:

- `models.py`
- `admin.py`
- `settings.py` -> `INSTALLED_APPS`, `ALLOWED_HOSTS`, `DATABASES`
- `urls.py`
- `views.py`

