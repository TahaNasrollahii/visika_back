from rest_framework import serializers
from .models import Category, Product, ProductFeature

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'title', 'value']

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'icon', 'color', 'image']

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    discountPrice = serializers.IntegerField(source='discount_price', read_only=True)
    is_favorite = serializers.SerializerMethodField()
    features = ProductFeatureSerializer(many=True, read_only=True)
    brand = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discountPrice', 'image', 'badge', 'is_best_seller', 'is_hot_offer', 'is_favorite', 'features', 'brand']

    def get_brand(self, obj):
        return obj.vendor.name if obj.vendor else "متفرقه"

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.favorited_by.filter(id=request.user.id).exists()
        return False

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
