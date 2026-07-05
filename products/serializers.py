from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductFeature

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'title', 'value']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'icon', 'color']

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    discountPrice = serializers.IntegerField(source='discount_price', read_only=True)
    is_favorite = serializers.SerializerMethodField()
    features = ProductFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discountPrice', 'image', 'badge', 'is_best_seller', 'is_hot_offer', 'is_favorite', 'features', 'brand']

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            # Assuming we can use obj.favorited_by or a prefetch
            return obj.favorited_by.filter(id=request.user.id).exists()
        return False

    def get_image(self, obj):
        image_url = obj.image
        if image_url:
            return image_url
        return None
