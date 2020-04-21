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

---> Isso vai lockar o projeto na apresentação (demora ~ 1 minuto)
---> Ativar o black., isort, mas não o mypy

```python
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

class BookStore(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=200)
    cnpj = models.CharField(blank=False, null=False, max_length=30)

    def __str__(self):
        return self.name

class Book(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=200)
    qty = models.IntegerField(default=0)

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

Mostrar os admins:

---> ```docker-compose up app```

## Health Check

`urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("healthcheck/", include("health_check.urls")),
]
```

`settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core",
    "health_check",
    "health_check.db",
]
```

http://0.0.0.0:8000/healthcheck/

## API

`settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core",
    "health_check",
    "health_check.db",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}
```

`views.py`

```python
from core.models import Book, BookStore
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


class BookStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStore
        fields = "__all__"


class BookStoreViewSet(viewsets.ModelViewSet):

    queryset = BookStore.objects.all()
    serializer_class = BookStoreSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    # extra: authentication
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    filter_fields = ("name", "cnpj")
    search_fields = ("name", "cnpj")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    # extra: authentication
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    filter_fields = ("name", "book_store", "qty")
    search_fields = ("name", "book_store", "qty")
```

`urls.py`

```python
from django.contrib import admin
from django.urls import path, include


from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register("book-store", views.BookStoreViewSet)
router.register("book", views.BookViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("healthcheck/", include("health_check.urls")),
    path("api/v1/", include(router.urls)),
]
```

---> Create some stores and books on admin

## Testing

### 1. MODELS

```python
from core.models import Book, BookStore
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class BookStoreTestCase(TestCase):
    def test_should_create_two_stores(self):
        BookStore.objects.create(cnpj="cnpj_1", name="store_1")
        BookStore.objects.create(cnpj="cnpj_2", name="store_2")

        self.assertEqual(BookStore.objects.count(), 2)


class BookTestCase(TestCase):

    # Test case related variables
    @classmethod
    def setUpTestData(cls):
        cls.book_store_1 = BookStore.objects.create(cnpj="cnpj_1", name="store_1")

    def test_should_create_a_book_related_to_a_book_store(self):
        # creation
        book_1 = Book.objects.create(name="book_1", qty=5, book_store=self.book_store_1)
        saved_book = Book.objects.get(id=book_1.id)

        # assertions
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(saved_book.name, "book_1")
        self.assertEqual(saved_book.book_store_id, self.book_store_1.id)
```

### 2. REST API

```python
from core.models import Book, BookStore
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class RestApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Shared data through all the texts ~ fixture!
        """
        cls.book_store_1 = BookStore.objects.create(cnpj="cnpj_1", name="store_1")
        cls.book_store_2 = BookStore.objects.create(cnpj="cnpj_2", name="store_2")

        cls.book_1_store_1 = Book.objects.create(
            book_store=cls.book_store_1, name="book_1", qty=2
        )
        cls.book_2_store_1 = Book.objects.create(
            book_store=cls.book_store_1, name="book_2", qty=4
        )

        # authentication
        cls.partner_user = User.objects.create(username="partner", password="partner")
        cls.partner_token = Token.objects.create(user=cls.partner_user)

    def setUp(self):
        self.client = APIClient()  # REST framework's test client
        # self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.partner_token.key}")

    # HTTP GET -- with and without query strings -- assertion with HTTP 200
    def test_should_get_a_list_of_stores_http_200(self):
        # self.client.get(reverse("book-store-endpoint-list"))
        response = self.client.get("/api/v1/book-store/")
        json_response = response.json()

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 2)
        self.assertEqual(json_response["results"][0]["cnpj"], "cnpj_1")

    def test_should_filter_book_stores_by_book_store_name_query_string_http_200(self):
        query_string_params = {"cnpj": "cnpj_2"}

        response = self.client.get("/api/v1/book-store/", query_string_params)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["cnpj"], "cnpj_2")

    def test_should_get_a_specific_store_http_200(self):
        response = self.client.get(f"/api/v1/book-store/{self.book_store_2.id}/")
        json_response = response.json()

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["cnpj"], "cnpj_2")

    # HTTP POST -- assertion with HTTP 201
    def test_should_create_book_from_store_1_http_201(self):
        book_data = {
            "name": " book_3",
            "qty": 3,
            "book_store": str(self.book_store_1.id),
        }

        response = self.client.post(f"/api/v1/book/", book_data)
        json_response = response.json()

        # assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response["name"], "book_3")
        self.assertEqual(
            Book.objects.filter(name="book_3", book_store__name="store_1").count(), 1
        )  # created successfully!

    # HTTP POST -- malformed -- assertion with HTTP 400
    def test_should_not_create_book_from_store_1_due_to_malformed_request_http_400(
        self,
    ):
        book_data = {
            # "name": " book_3",
            "qty": 3,
            "book_store": str(self.book_store_1.id),
        }

        response = self.client.post(f"/api/v1/book/", book_data)
        json_response = response.json()

        # assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            Book.objects.filter(name="book_3", book_store__name="store_1").count(), 0
        )  # NO creation

    # HTTP PUT -- assertion with HTTP 200
    def test_should_update_book_from_store_1_http_200(self):
        book_update_data = {
            "name": "book_4",
            "book_store": str(self.book_store_1.id),
            "qty": 10,
        }

        book_for_update = Book.objects.create(
            name="book_4", qty=0, book_store=self.book_store_1
        )

        response = self.client.put(
            f"/api/v1/book/{book_for_update.id}/", book_update_data,
        )

        # assertions
        self.assertEqual(response.status_code, 200)
        updated_book = Book.objects.get(id=book_for_update.id)
        self.assertEqual(updated_book.qty, 10)
```

### 3. Rest API com autenticação

--> apresentar o `rest_framework.authtoken` no admin
--> descomentar as autenticações/permissões nas modelviewsets
--> ver testes quebrar com 401
--> login o client de test e fazer os testes passarem
