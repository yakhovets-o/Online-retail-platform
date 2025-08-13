from django.contrib import admin
from unfold.admin import (
    ModelAdmin,
)  # Замена from django.contrib import admin.ModelAdmin

from .models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    """
    Admin interface for User models.
    Displays:
    - `username`
    - `email`
    - `is_staff`
    - `is_active`

    Filters:
    - `is_staff`
    - `is_superuser`
    - `is_active`

    Search:
    - `username`
    - `email`
    """

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
