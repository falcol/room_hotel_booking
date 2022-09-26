from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class BaseUser(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser',
                    'is_active')
    list_filter = ('username', )
