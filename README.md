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

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core"
]

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
