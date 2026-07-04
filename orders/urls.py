from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartRetrieveUpdateView.as_view(), name='cart-detail'),
    path('cart/items/', views.CartItemAddView.as_view(), name='cart-item-add'),
    path('cart/items/<int:pk>/', views.CartItemUpdateDeleteView.as_view(), name='cart-item-detail'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
