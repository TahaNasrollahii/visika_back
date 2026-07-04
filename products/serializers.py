from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'icon', 'color']

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    discountPrice = serializers.IntegerField(source='discount_price', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discountPrice', 'image', 'badge', 'is_best_seller', 'is_hot_offer']

    def get_image(self, obj):
        image_url = obj.image
        if image_url:
            return image_url
        return None
