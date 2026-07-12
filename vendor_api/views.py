from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsVendor
from products.models import Product
from orders.models import OrderItem
from users.models import Notification, User
from .serializers import VendorProductSerializer, VendorOrderSerializer, NotificationSerializer, VendorNotificationHistorySerializer

class VendorProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsVendor]
    serializer_class = VendorProductSerializer

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor)

class VendorOrderListView(generics.ListAPIView):
    permission_classes = [IsVendor]
    serializer_class = VendorOrderSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(product__vendor=self.request.user.vendor).order_by('-created_at')

class VendorSendNotificationView(APIView):
    permission_classes = [IsVendor]

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            recipient = serializer.validated_data['recipient']
            
            # Verify that the recipient has ordered from this vendor
            has_ordered = OrderItem.objects.filter(
                order__user=recipient,
                product__vendor=request.user.vendor
            ).exists()

            if not has_ordered:
                return Response(
                    {"error": "You can only send notifications to customers who have ordered your products."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(sender=request.user.vendor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorNotificationHistoryView(generics.ListAPIView):
    permission_classes = [IsVendor]
    serializer_class = VendorNotificationHistorySerializer

    def get_queryset(self):
        return Notification.objects.filter(sender=self.request.user.vendor).order_by('-created_at')
