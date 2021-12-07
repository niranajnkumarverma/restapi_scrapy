from django.db.models import fields
from rest_framework import serializers

from .models import *

class FirstSerializers(serializers.Serializer):
    '''Serialize a name field for testing our APIView'''

    name = serializers.CharField(max_length=20)

class ProfileSerializer(serializers.ModelSerializer):
    '''Serializes a user profile object'''

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
    
    def create(self, validated_data):
        '''create and return a new user'''

        user = UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user

class TaskSerializer(serializers.Serializer):
    '''serializes user tasks'''

    class Meta:
        model = Task
        fields = ('id', 'user_profile', 'Title', 'Description')
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }