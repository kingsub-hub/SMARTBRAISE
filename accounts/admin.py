from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile, LoginHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    model = User

    ordering = ["-date_joined"]

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "email_verified",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "email_verified",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    fieldsets = (
        (
            "Informations de connexion",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),

        (
            "Informations personnelles",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "date_of_birth",
                    "bio",
                    "avatar",
                )
            },
        ),

        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),

        (
            "Dates importantes",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
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
                    "role",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "city",
        "country",
    )

    search_fields = (
        "user__email",
        "city",
        "country",
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "timestamp",
        "ip_address",
        "success",
    )

    list_filter = (
        "success",
        "timestamp",
    )

    search_fields = (
        "user__email",
        "ip_address",
    )

    readonly_fields = (
        "timestamp",
    )