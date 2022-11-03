from django.contrib import admin

from .models import Comments, CustomerDetails

# Register your models here.


@admin.register(CustomerDetails)
class CustomerAdmin(admin.ModelAdmin):
    # form = CustomerDetailsForm
    pass


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    # form = CustomerDetailsForm
    pass
