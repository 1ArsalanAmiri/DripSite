from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductImageViewSet , CollectionViewSet , ProductVariantViewSet

router = DefaultRouter()
router.register(r'product-list', ProductViewSet)
router.register(r'product-images', ProductImageViewSet),
router.register(r'product-collection', CollectionViewSet),
router.register('product-variants', ProductVariantViewSet),

urlpatterns = router.urls
