from django.db import models

# Create your models here.

class Student(models.Model):
 name  = models.CharField(max_length=50)
 roll = models.IntegerField(max_length=100)
 city = models.CharField(max_length=50)
 state = models.CharField(max_length=50)
