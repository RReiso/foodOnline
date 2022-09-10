from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'role', 'is_active')  # which fields will be displatyed in admin panel
    ordering = ('-date_joined',)
    filter_horizontal = ()  # adds a search field in admin panel
    list_filter = ("is_admin",)  # adds filter window on the right side
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)  # will be visible in admin panel
admin.site.register(UserProfile)
