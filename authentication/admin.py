from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .forms import UserRegisterForm


# Register your models here.
class BaseUser(UserAdmin):
    add_form = UserRegisterForm

    model = User

    list_display = (
        'username',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (('UserInfo', {
        'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'name')
    }), ('Permissions', {
        'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
    }), ('Dates', {
        'fields': ('last_login', 'date_joined')
    }))
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')
    }),)
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, BaseUser)
