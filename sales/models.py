from django.db import models

class SalesRecord(models.Model):
    date = models.DateField()
    region = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.region} - {self.product} - {self.date} - {self.quantity} x {self.price}"
