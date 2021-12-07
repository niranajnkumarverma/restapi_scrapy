from django.db import models

# Create your models here.
class NewUser(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=12)

    