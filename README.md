# Fast API

## Pre requisito 

- Python
- Django (pip install django)

## Inicio

Iniciando um projeto Django

```bash
django-admin startproject fast_api .
```

Executando

```bash
python manage.py runserver 
```

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

Criando uma aplicação

```bash
python manage.py startapp core
```

-----> open -na "PyCharm.app" .

adicionar Dockerfile

```
FROM python:3.8.2-buster

WORKDIR /web

COPY . /web

RUN pip install -r requirements.txt

```

Adicionar docker-compose.yml

```yml 
version: "3.7"
services:
  db:
    image: postgres:10.1-alpine
  app:
    build:
      context: .
    env_file: .env
    volumes:
      - .:/app
    working_dir: /app
    ports:
      - "8000:8000"
    depends_on:
      - db
    command:
      [
        "./wait-for-it.sh",
        "${DB_HOST}:${DB_PORT}",
        "-t",
        "120",
        "--",
        "./start.sh",
      ]
```

Adicionar requirements.txt

```
django==3.0.5
django-health-check==3.4.1
django-filter==2.2.0
djangorestframework==3.11.0
psycopg2-binary==2.8.5

```

Adicionar .env

```
##################
#### Database engine
DB_ENGINE=django.db.backends.postgresql
DB_DATABASE=postgres
DB_USER=postgres
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
```

Adicionar start.sh

```bash 
#!/bin/bash
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000
```

Adicionar wait-for-it.sh
https://raw.githubusercontent.com/ricardochaves/financeiro-bot/master/wait-for-it.sh

Rodar `chmod +x`


Rodar build para cirar as imagens

```bash
docker-compose build 
```

-----> Confirgurar interpretador

Enquanto ele fazer o build e o interpretador vamos criando as classes:

```python 
from django.db import models

class BookStore(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(blank=False, null=False, max_length=200)
    cnpj = models.CharField(blank=False, null=False, max_length=30)

    def __str__(self):
        return self.name


class Book(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(blank=False, null=False, max_length=200)
    qtd = models.IntegerField(default=0)

    book_store = models.ForeignKey(BookStore, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
```

Configurar `settings.py`

```python 
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_DATABASE"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

```

Configurar `admin.py`

```python 
from django.contrib import admin

from core.models import BookStore, Book


@admin.register(BookStore)
class BookStoreAdmin(admin.ModelAdmin):
    list_display = (
        "cnpj",
        "name",
    )
    list_filter = (
        "created_at",
        "updated_at"
    )

    admin_order_field = "-created_at"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    list_filter = (
        "created_at",
        "updated_at"
    )

    admin_order_field = "-created_at"

```
