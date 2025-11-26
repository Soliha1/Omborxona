from django.db import models


class Branch(models.Model):
    name=models.CharField()
    details=models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField()
    brand=models.CharField(blank=True, null=True)
    price=models.FloatField(blank=True, null=True)
    quantity=models.FloatField(default=0)
    unit=models.CharField()
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Client(models.Model):
    name=models.CharField()
    shop_name=models.CharField(blank=True, null=True)
    phone_number=models.CharField()
    address=models.TextField()
    debt=models.FloatField(default=0)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

