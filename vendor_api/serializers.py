from rest_framework import serializers
from products.models import Product, ProductFeature
from orders.models import OrderItem, Order
from users.models import Notification

class VendorProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'title', 'value']

class VendorProductSerializer(serializers.ModelSerializer):
    features = VendorProductFeatureSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discount_price', 'category', 'image', 'image_url', 'badge', 'is_best_seller', 'is_hot_offer', 'brand', 'stock', 'features']
        read_only_fields = ['id']

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class VendorOrderSerializer(serializers.ModelSerializer):
    customer_phone = serializers.CharField(source='order.user.phone_number', read_only=True)
    customer_name = serializers.CharField(source='order.user.full_name', read_only=True)
    customer_id = serializers.IntegerField(source='order.user.id', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    order_status = serializers.CharField(source='order.status', read_only=True)
    order_date = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'customer_id', 'customer_name', 'customer_phone', 'product', 'product_title', 'quantity', 'price', 'delivery_time', 'order_status', 'order_date']
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
