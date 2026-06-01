from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Painting, Cart, Order, OrderItem, ContactSubmission, SiteSettings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'user_type', 'is_staff', 'date_joined']
    list_filter = ['user_type', 'is_staff']
    search_fields = ['email', 'username']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_available', 'sold_count']
    list_filter = ['category', 'is_available']


admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ContactSubmission)
admin.site.register(SiteSettings)
