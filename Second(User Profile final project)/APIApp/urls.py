from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('first-viewset', views.MyViewSet, basename='first-viewset')
router.register('profile', views.ProfileViewSet)
router.register('task', views.TaskViewSet)

urlpatterns = [
    path('api-view/', views.MyApiView.as_view()),
    path('', include(router.urls)),
]