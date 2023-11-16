from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    phone_number=models.IntegerField(null=True)
    username=models.CharField(unique=True,max_length=100,null=True)
    gold=models.IntegerField(default=0)
    sand=models.DateTimeField(default=datetime(2023,10,27,12,5,30))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self) -> str:
        return str(self.email)

class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_item = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.data_item
