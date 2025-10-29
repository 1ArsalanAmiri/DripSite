from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Product, ProductImage, Collection , ProductVariant
from .serializers import ProductSerializer, ProductImageSerializer, CollectionSerializer , ProductVariantSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related('images')
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except Exception as e:
            return Response(
                {"error": f"There Is a Error While Creating Your Object : {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all().prefetch_related('products')
    serializer_class = CollectionSerializer
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except Exception as e:
            return Response(
                {"error": f"There is an error in your request: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)