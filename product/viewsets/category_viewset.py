from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from product.models import Category
from product.serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return Category.objects.all()