from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__phone_number',)
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    search_fields = ('user__phone_number', 'id')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
