from django.contrib.gis.db import models
import uuid
import datetime

# Create your models here.
class Excel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f'File id: {str(self.id)}'



class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.PositiveBigIntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    geom = models.MultiPointField(srid=4326, null=True, blank=True)

    def __str__(self): return str(self.customer_name)



class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    product_a = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    product_b = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    product_c = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    total_sales = models.PositiveSmallIntegerField(default=0, null=True, blank=True)


    def __str__(self): return f'Sale by {str(self.customer.customer_name)}'

    def save(self, *args, **kwargs):
        self.total_sales = self.product_a + self.product_b + self.product_c
        super().save(*args, **kwargs)



class Ward(models.Model):
    county = models.CharField(max_length=25)
    sub_county = models.CharField(max_length=25)
    ward = models.CharField(max_length=25)
    geom = models.MultiPolygonField(srid=4326)

    ward_url = models.CharField(max_length=100)

    def __str__(self): return self.ward

    def save(self, *args, **kwargs):
        self.ward_url = str(self.ward).lower().replace(" ","_").replace("'","").replace('/', '-')
        super().save(*args, **kwargs)
        