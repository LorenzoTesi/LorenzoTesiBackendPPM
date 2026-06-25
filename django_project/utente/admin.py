from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Ruoli Progetto', {'fields': ('is_organizer',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)