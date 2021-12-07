from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import NewUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('id', 'name', 'email', 'password')