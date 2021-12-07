from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import *

# Create your views here.

def index(request):
    return HttpResponse("<h1>RestAPI Framework Page</h1>")


@api_view(['GET', 'POST'])
def all_users(request):
    if request.method == 'GET':
        users = NewUser.objects.all()
        print(users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        new_data = {'name': request.POST.get('name'), 'email': request.POST.get('email')}
        print(new_data)
        serializer = UserSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)