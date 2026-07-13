import json
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from products.models import Product, ProductFeature
from orders.models import OrderItem, Order
from users.models import Notification, VendorDeliveryRule
from shopping.models import BasketRule

class VendorProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'title', 'value']

class VendorProductSerializer(serializers.ModelSerializer):
    features = VendorProductFeatureSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    features_data = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discount_price', 'category', 'image', 'image_url', 'badge', 'is_best_seller', 'is_hot_offer', 'stock', 'features', 'features_data']
        read_only_fields = ['id']

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def create(self, validated_data):
        features_data = validated_data.pop('features_data', None)
        product = super().create(validated_data)
        if features_data:
            try:
                features = json.loads(features_data)
                for f in features:
                    if f.get('title') and f.get('value'):
                        ProductFeature.objects.create(product=product, title=f['title'], value=f['value'])
            except json.JSONDecodeError:
                pass
        return product

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features_data', None)
        product = super().update(instance, validated_data)
        if features_data is not None:
            try:
                features = json.loads(features_data)
                instance.features.all().delete()
                for f in features:
                    if f.get('title') and f.get('value'):
                        ProductFeature.objects.create(product=product, title=f['title'], value=f['value'])
            except json.JSONDecodeError:
                pass
        return product

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


class VendorNotificationHistorySerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.full_name', read_only=True)
    recipient_phone = serializers.CharField(source='recipient.phone_number', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient_name', 'recipient_phone', 'message', 'is_read', 'created_at']



WEEKDAY_FIELDS = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

class VendorDeliveryRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDeliveryRule
        fields = [
            'preparation_days',
            'end_of_order_taking_hour',
            *WEEKDAY_FIELDS,
        ]

class BasketRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketRule
        fields = ['min_order_price', 'min_order_quantity']

    def validate_min_order_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(_("Minimum order price cannot be negative."))
        return value

    def validate_min_order_quantity(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(_("Minimum order quantity cannot be negative."))
        return value
