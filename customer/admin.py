from django.contrib import admin

from .models import CustomerDetails

# Register your models here.


@admin.register(CustomerDetails)
class CustomerAdmin(admin.ModelAdmin):
    # form = CustomerDetailsForm
    pass
