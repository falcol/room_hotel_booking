from django.db import models


# Create your models here.
class Payment(models.Model):

    order_id = models.CharField(max_length=250)
    order_type = models.CharField(max_length=20)
    amount = models.IntegerField()
    order_desc = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id
