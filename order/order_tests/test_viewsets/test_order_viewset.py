import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from order.models import Order

class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)[0]
        self.assertEqual(order_data['results'][0]['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['results'][0]['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['results'][0]['product'][0]['active'], self.product.active)
        self.assertEqual(order_data['results'][0]['product'][0]['category'][0]['title'], self.category.title)
        self.assertEqual(order_data['total'], self.product.price)

    def test_create_order(self):
        user = UserFactory()
        category = CategoryFactory()
        product = ProductFactory(category=[category], price=100)
        data = {
            'products_id': [product.id],
            'user': user.id
        }

        response = self.client.post(
            reverse('order-list'),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('total', response.data)
        self.assertEqual(response.data['total'], 100)

        created_order = Order.objects.get(user=user)
        self.assertEqual(created_order.product.first().title, product.title)
        self.assertEqual(created_order.product.first().price, 100)
        self.assertEqual(created_order.product.count(), 1)
