from django.urls import path, include
from rest_framework.routers import DefaultRouter 

from product.viewsets import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
