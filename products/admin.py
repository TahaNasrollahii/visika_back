from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, Product, ProductFeature

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

class ProductFeatureInline(TabularInline):
    model = ProductFeature
    extra = 1

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('title', 'category', 'price', 'vendor', 'is_best_seller', 'is_hot_offer')
    search_fields = ('title', 'description', 'badge', 'vendor__name')
    list_filter = ('category', 'is_best_seller', 'is_hot_offer')
    inlines = [ProductFeatureInline]
    readonly_fields = ('created_at', 'updated_at')
    fields = (
        'title', 'description', 'category', 'vendor',
        'image',
        'price', 'discount_price', 'badge',
        'is_best_seller', 'is_hot_offer',
        'created_at', 'updated_at',
    )
