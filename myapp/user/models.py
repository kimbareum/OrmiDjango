from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=255)
    registered_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255, unique=False)

    USERNAME_FIELD = 'email'
    # AbstractUser를 상속받으면 필수값을 지정가능함
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

