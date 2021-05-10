from django.contrib import admin

from .models import (
    Excel,
    Sale,
    Customer,
    Ward,
)

# Register your models here.
admin.site.register(Excel)
admin.site.register(Sale)
admin.site.register(Customer)
admin.site.register(Ward)