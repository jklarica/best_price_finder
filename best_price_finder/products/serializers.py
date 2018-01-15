from rest_framework import serializers

from products.models import Product, PricingBlock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'currency', 'name', 'published')


class PricingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingBlock
        fields = ('id', 'start_date', 'end_date', 'nights', 'price', 'product_id')


class BestPriceSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    currency = serializers.CharField(max_length=3, required=False)
    blocks = PricingBlockSerializer(many=True, required=False)
