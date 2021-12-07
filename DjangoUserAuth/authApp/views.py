from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User#, PermissionsMixin

# Create your views here.
def index(request):
    return HttpResponse("<h1>hello from first view</h1>")

def new_user(request):
    user = User.objects.create_user('user_two', 'user_two@mail.com', 'uo@pass21')

    user.is_superuser = True
    user.is_staff = True
    user.save()

    return HttpResponse(user)

def all_user(request):
    user = User.objects.all()


    return JsonResponse({'users': 'niranjan', 'age': 20})