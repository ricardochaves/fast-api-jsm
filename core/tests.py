from core.models import Book, BookStore
from django.test import TestCase


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
        book_1 = Book.objects.create(name="book_1", qtd=5, book_store=self.book_store_1)
        saved_book = Book.objects.get(id=book_1.id)

        # assertions
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(saved_book.name, "book_1")
        self.assertEqual(saved_book.book_store_id, self.book_store_1.id)
