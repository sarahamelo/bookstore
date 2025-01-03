from django.urls import path, include
from rest_framework import routers

from order import viewsets

router = routers.SimpleRouter()
router.register(r'order', viewsets.OrderViewSet, basename='order')

urlpatterns = [
    path('<str:version>/', include(router.urls)),
]