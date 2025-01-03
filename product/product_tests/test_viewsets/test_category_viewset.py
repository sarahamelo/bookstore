import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from product.models import Category

class TestCategoryViewSet(APITestCase):  # Certifique-se do nome correto da classe
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="Electronics")
        self.product = ProductFactory(
            title="mouse",
            price=100,
            category=[self.category]
        )

    def test_get_all_category(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        category_data = json.loads(response.content)
        
        # Verifique se há dados antes de acessar
        self.assertIn('results', category_data)
        self.assertGreater(len(category_data['results']), 0)

        self.assertEqual(category_data['results'][0]['title'], self.category.title)


    def test_create_category(self):
        data = {
            "title": "technology",
            "slug": "technology",
            "description": "A tech category",
            "active": True
        }

        response = self.client.post(
            reverse('category-list'),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title='technology')

        self.assertEqual(created_category.title, 'technology')
