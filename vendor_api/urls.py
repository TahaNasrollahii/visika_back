from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorProductViewSet, VendorOrderListView, VendorSendNotificationView,
    VendorNotificationHistoryView, VendorDeliveryRuleView, VendorBasketRuleView,
)

router = DefaultRouter()
router.register(r'products', VendorProductViewSet, basename='vendor-products')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', VendorOrderListView.as_view(), name='vendor-orders'),
    path('notifications/send/', VendorSendNotificationView.as_view(), name='vendor-send-notification'),
    path('notifications/history/', VendorNotificationHistoryView.as_view(), name='vendor-notification-history'),
    path('delivery-rule/', VendorDeliveryRuleView.as_view(), name='vendor-delivery-rule'),
    path('basket-rule/', VendorBasketRuleView.as_view(), name='vendor-basket-rule'),
]
