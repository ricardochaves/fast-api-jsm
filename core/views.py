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


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
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


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    # extra: authentication
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    filter_fields = ("name", "book_store", "qty")
    search_fields = ("name", "book_store", "qty")
