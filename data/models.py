from django.contrib.gis.db import models
import uuid
import datetime

# Create your models here.
class Excel(models.Model):
    file = models.FileField(upload_to='uploads/')
    created = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self): return f'File id: {str(self.id)}'



class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    product_a = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    product_b = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    product_c = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

    def __str__(self): return str(self.id)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.PositiveBigIntegerField(null=True, blank=True)
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    geom = models.MultiPointField(srid=4326, null=True, blank=True)

    def __str__(self): return str(self.customer_name)