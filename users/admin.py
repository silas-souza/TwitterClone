from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Perfil", {"fields": ("profile_picture",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Perfil", {"fields": ("profile_picture",)}),
    )