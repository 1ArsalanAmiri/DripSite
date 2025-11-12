from django.shortcuts import redirect
from django.urls import path
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductImageViewSet , CollectionViewSet , ProductVariantViewSet


def redirect_to_products(request):
    return redirect('/api/products/')

router = DefaultRouter()

router.register(r'product-list', ProductViewSet , basename='product-list')
router.register(r'product-images', ProductImageViewSet),
router.register(r'product-collection', CollectionViewSet),
router.register('product-variants', ProductVariantViewSet),


urlpatterns = router.urls + [
    path('products/', redirect_to_products, name='product-list'),
]