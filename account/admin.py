from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Role


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('email', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email','first_name','last_name','roles', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name','roles', 'password1', 'password2', 'is_staff', 'is_active', )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
