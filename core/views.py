from core.models import BookStore
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter


class BookStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStore
        fields = "__all__"


class BookStoreViewSet(viewsets.ModelViewSet):

    queryset = BookStore.objects.all()

    serializer_class = BookStoreSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    filter_fields = ("name", "cnpj")
    search_fields = ("name", "cnpj")
