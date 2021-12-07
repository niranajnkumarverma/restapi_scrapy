from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('all_users/', all_users, name='all_users'),
]