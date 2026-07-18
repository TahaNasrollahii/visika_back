from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from users.permissions import IsCustomer
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer

class CartRetrieveUpdateView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartItemAddView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsCustomer]

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

class CheckoutView(generics.CreateAPIView):
    permission_classes = [IsCustomer]

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        from shopping.models import BasketRule
        vendor_ids = set(
            cart.items.exclude(product__vendor__isnull=True)
            .values_list('product__vendor_id', flat=True)
        )
        for vendor_id in vendor_ids:
            try:
                rule = BasketRule.objects.get(vendor_id=vendor_id)
            except BasketRule.DoesNotExist:
                continue
            try:
                rule.validate_basket_conditions(cart)
            except ValidationError as e:
                return Response(
                    {"error": "; ".join(e.messages)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            status='paid' # Mocking payment success
        )

        delivery_times = request.data.get('delivery_times', {})

        for item in cart.items.all():
            brand = item.product.vendor.name if item.product and item.product.vendor else "متفرقه"
            delivery_time = delivery_times.get(brand, "")
            
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discount_price if item.product.discount_price else item.product.price,
                delivery_time=delivery_time
            )
            
            # Reduce product stock
            if item.product.stock > 0:
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()
        
        cart.items.all().delete()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderRetrieveView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


from rest_framework.views import APIView
from users.models import Vendor, VendorDeliveryRule

class VendorDeliveryInfoView(APIView):
    """
    Public endpoint for customers to fetch delivery rules for specific vendors.
    Query params: ?brands=BrandA,BrandB
    Returns a dict mapping vendor name -> delivery rule info.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brands_param = request.query_params.get('brands', '')
        if not brands_param:
            return Response({}, status=status.HTTP_200_OK)

        brand_names = [b.strip() for b in brands_param.split(',') if b.strip()]
        vendors = Vendor.objects.filter(name__in=brand_names).select_related('delivery_rule')

        result = {}
        for vendor in vendors:
            try:
                rule = vendor.delivery_rule
                result[vendor.name] = {
                    'preparation_days': rule.preparation_days,
                    'end_of_order_taking_hour': rule.end_of_order_taking_hour,
                    'saturday': rule.saturday,
                    'sunday': rule.sunday,
                    'monday': rule.monday,
                    'tuesday': rule.tuesday,
                    'wednesday': rule.wednesday,
                    'thursday': rule.thursday,
                    'friday': rule.friday,
                }
            except VendorDeliveryRule.DoesNotExist:
                # Vendor has no delivery rule — use defaults
                result[vendor.name] = {
                    'preparation_days': 2,
                    'end_of_order_taking_hour': 15,
                    'saturday': True,
                    'sunday': True,
                    'monday': True,
                    'tuesday': True,
                    'wednesday': True,
                    'thursday': True,
                    'friday': False,
                }

        return Response(result, status=status.HTTP_200_OK)
