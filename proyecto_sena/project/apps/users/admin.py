# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import customuser
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(customuser, CustomUserAdmin)
