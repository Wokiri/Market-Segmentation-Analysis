from django.contrib import admin

from .models import (
    Excel,
    Sale,
    Customer
)

# Register your models here.
admin.site.register(Excel)
admin.site.register(Sale)
admin.site.register(Customer)
