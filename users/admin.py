from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User, Address

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'status', 'is_staff', 'is_superuser')
    search_fields = ('phone_number', 'first_name', 'last_name', 'national_id')
    list_filter = ('status', 'is_staff', 'is_superuser', 'gender', 'is_phone_verified')
    filter_horizontal = ('favorites', 'groups', 'user_permissions')
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('title', 'user', 'is_default', 'created_at')
    search_fields = ('title', 'user__phone_number', 'user__first_name', 'user__last_name', 'postal_code')
    list_filter = ('is_default', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
