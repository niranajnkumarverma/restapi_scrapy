from django.urls import path
from .views import index, new_user, all_user

urlpatterns = [
    path('', index),
    path('new/', new_user, name="new_user"),
    path('all_users/', all_user, name='all_users'),
]