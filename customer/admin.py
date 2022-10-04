from django.contrib import admin
from .models import CustomerDetails
from .forms import CustomerDetailsForm
# Register your models here.


@admin.register(CustomerDetails)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerDetailsForm
    pass
