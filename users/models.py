from django.db import models
from django.contrib.auth.models import AbstractUser, User
from main.models import Branch

class User(AbstractUser):
    phone_number=models.CharField(blank=True,  null=True)
    description=models.TextField(blank=True, null=True)
    branch=models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)


