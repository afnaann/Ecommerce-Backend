from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_active",
        "is_blocked",
    )  # Specify the fields to display in the list view
    list_filter = ("is_staff", "is_active")  # Add filter options
    search_fields = ("email",)  # Add search functionality
    ordering = ("email",)  # Specify default ordering

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    # Set the USERNAME_FIELD to email for login
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# Register the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
