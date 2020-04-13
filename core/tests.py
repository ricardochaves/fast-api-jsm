from core.models import Book, BookStore
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.utils import json


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


class BookStoreApiTestCase(TestCase):

    # Test case related variables
    @classmethod
    def setUpTestData(cls):
        cls.book_store_1 = BookStore.objects.create(cnpj="cnpj_1", name="store_1")
        cls.book_store_2 = BookStore.objects.create(cnpj="cnpj_2", name="store_2")

        cls.book_1_store_1 = Book.objects.create(
            book_store=cls.book_store_1, name="book_1", qty=2
        )
        cls.book_2_store_1 = Book.objects.create(
            book_store=cls.book_store_1, name="book_2", qty=4
        )

    def test_should_get_a_list_of_stores_http_200(self):
        # self.client.get(reverse("book-store-endpoint-list"))
        response = self.client.get("/api/v1/book-store/")
        json_response = response.json()

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 2)
        self.assertEqual(json_response["results"][0]["cnpj"], "cnpj_1")

    def test_should_get_a_specific_store_http_200(self):
        response = self.client.get(f"/api/v1/book-store/{self.book_store_2.id}/")
        json_response = response.json()

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["cnpj"], "cnpj_2")
