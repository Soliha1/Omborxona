from django.db import models
from main.models import Product, Branch, Client
from users.models import User


class importproduct(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.FloatField()
    buy_price=models.FloatField()

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)


    def totak_price(self):
        return self.buy_price * self.quantity


class Sale(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    quantity=models.FloatField(default=1)
    total_price=models.FloatField(default=0)
    paid_price=models.FloatField(default=0)
    debt_price=models.FloatField(default=0)

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)

class PayDebt(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    price=models.FloatField()
    description=models.TextField(blank=True, null=True)

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)

