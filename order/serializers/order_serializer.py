from rest_framework import serializers
from order.models.order import Order
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    products_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        return sum(product.price for product in instance.product.all())

    class Meta:
        model = Order
        fields = ['id', 'product', 'user', 'products_id', 'total']
        extra_kwargs = {'product': {'required': False}}

    def create(self, validated_data):
        products_id = validated_data.pop('products_id')
        user = validated_data.get('user')

        order = Order.objects.create(user=user)
        order.product.set(products_id)

        return order
