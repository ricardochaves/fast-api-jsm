from core.models import Book, BookStore
from django.contrib import admin


@admin.register(BookStore)
class BookStoreAdmin(admin.ModelAdmin):
    list_display = (
        "cnpj",
        "name",
    )
    list_filter = ("created_at", "updated_at")

    admin_order_field = "-created_at"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("created_at", "updated_at")

    admin_order_field = "-created_at"
