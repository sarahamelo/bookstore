import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from rest_framework.authtoken.models import Token

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory
from product.models import Product

class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

        self.product = ProductFactory(
            title='pro controller',
            price=200,
        )

    def test_get_all_product(self):
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)
        
        # Verifique se há dados antes de acessar
        self.assertIn('results', product_data)
        self.assertGreater(len(product_data['results']), 0)

        self.assertEqual(product_data['results'][0]['title'], self.product.title)
        self.assertEqual(product_data['results'][0]['price'], self.product.price)


    def test_create_product(self):
        token, created = Token.objects.get_or_create(user=self.user)  # Verifica se já existe um token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        category = CategoryFactory()
        data = {
            'title': 'notebook',
            'price': 800,
            'category_id': [category.id]
        }

        response = self.client.post(
            reverse('product-list'),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title='notebook')

        self.assertEqual(created_product.title, 'notebook')
        self.assertEqual(created_product.price, 800)

