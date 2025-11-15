# yourapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Define a custom admin class to display additional fields
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Specify fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'usertype', 'is_staff')
    # Define fields to include when viewing/editing a user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('usertype', 'line1', 'city', 'state', 'pincode', 'pphoto')}),
    )
    # Define fields to include when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('usertype', 'line1', 'city', 'state', 'pincode', 'pphoto')}),
    )
    search_fields = ('username', 'email', 'usertype')
    ordering = ('username',)

# Register the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
