from re import search
from django.shortcuts import render
from rest_framework.serializers import Serializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

class MyApiView(APIView):
    '''my first api view'''

    serializer_class = serializers.FirstSerializers

    def get(self, request, format=None):
        '''return a list of APIView features'''

        an_apiview = [
            'User HTTP methods as function (get, post, patch, put, delete',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello! APIView. This is a first api view.', 'an_apiview': an_apiview})

    def post(self, request):
        '''create a message with our name'''

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello! {name}.'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        '''handle updating an object'''

        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        '''handle a partial update of an object'''

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        '''delete an object'''

        return Response({'method': 'DELETE'})

class MyViewSet(viewsets.ViewSet):
    '''only for testing API Viewset'''

    serializer_class = serializers.FirstSerializers,

    def list(self, request):
        '''return a message'''

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        '''create a new message'''

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello! {name}.'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        '''handle getting an object by its ID'''

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        '''handle updating an object'''

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        '''handle updating part of an object'''

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        '''handle removing an object'''

        return Response({'http_method': 'DELETE'})

class ProfileViewSet(viewsets.ModelViewSet):
    '''handle creating and updating user profiles'''

    serializer_class = serializers.ProfileSerializer

    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)

    permission_classes = (permissions.UpdateProfile,)

    filter_backends = (filters.SearchFilter,)

    search_fields = ('name', 'email',)

class TaskViewSet(viewsets.ModelViewSet):
    '''handle creating, reading, updating profile tasks'''

    serializer_class = serializers.TaskSerializer

    queryset = models.Task.objects.all()

    authentication_classes = (TokenAuthentication,)

    permission_classes = (permissions.UpdateTask,)

    def perform_create(self, serializer):
        '''sets the user profile to the logged in user'''

        serializer.save(user_profile=self.request.user)