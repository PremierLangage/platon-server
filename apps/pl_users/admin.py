from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from django.contrib.auth.forms import UserChangeForm


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomserAdmin(UserAdmin):
    form = CustomUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('is_editor', 'avatar',)}),
    )


admin.site.register(User, CustomserAdmin)
