from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, Product, ProductImage, ProductFeature

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(TabularInline):
    model = ProductFeature
    extra = 1

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('title', 'category', 'price', 'brand', 'rating', 'is_best_seller', 'is_hot_offer')
    search_fields = ('title', 'description', 'badge', 'brand')
    list_filter = ('category', 'is_best_seller', 'is_hot_offer', 'brand')
    inlines = [ProductImageInline, ProductFeatureInline]
    readonly_fields = ('created_at', 'updated_at')
