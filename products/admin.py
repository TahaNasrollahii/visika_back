from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discount_price', 'is_best_seller', 'is_hot_offer')
    search_fields = ('title', 'description', 'badge')
    list_filter = ('category', 'is_best_seller', 'is_hot_offer')
    inlines = [ProductImageInline]
    readonly_fields = ('created_at', 'updated_at')
