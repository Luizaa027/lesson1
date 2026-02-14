# from django.urls import path
# from apps.product.views import ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView

# urlpatterns = [
#     path("products/", ProductListAPIView.as_view(), name='product-list'),
#     path("products/<uuid:uuid>/", ProductDetailAPIView.as_view(), name='product-detail'),
#     path("product/create/", ProductCreateAPIView.as_view(), name='create'),
#     path("product", ProductCreateAPIView.as_view(), name='product_list'),
# ] 

from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ModelsViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'models', ModelsViewSet, basename='models')

urlpatterns = router.urls