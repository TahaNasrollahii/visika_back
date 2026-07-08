from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BasketRule

@admin.register(BasketRule)
class BasketRuleAdmin(ModelAdmin):
    list_display = ('vendor', 'min_order_price', 'min_order_quantity')
    search_fields = ('vendor__name',)
