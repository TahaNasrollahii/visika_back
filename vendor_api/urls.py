from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorProductViewSet, VendorOrderListView, VendorSendNotificationView

router = DefaultRouter()
router.register(r'products', VendorProductViewSet, basename='vendor-products')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', VendorOrderListView.as_view(), name='vendor-orders'),
    path('notifications/send/', VendorSendNotificationView.as_view(), name='vendor-send-notification'),
]
