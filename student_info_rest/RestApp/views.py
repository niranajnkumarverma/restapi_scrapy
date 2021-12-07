from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import serializers
from .models import Student
from .serializers import StudentSerializers
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse #jsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

def student_Detail(request):
    stu = Student.objects.get(id=1)
    # print(stu)
    serializer = StudentSerializers(stu)
    # print(seializers)
    # print(serializers.data)
    json_data = JSONRenderer().render(serializer.data) # this part hide
    # print(json_data)
    return HttpResponse(json_data, content_type = 'application/json') #this part hide
   # return JsonResponse(serializer.data)

# Queryset All Student_data

def student_list(request):
    stu = Student.objects.all()
    # print(stu)
    serializers = StudentSerializers(stu,many =True )
    # print(seializers)
    # print(serializers.data)
    json_data = JSONRenderer().render(serializers.data) #this part hide for short
    # print(json_data)
    return HttpResponse(json_data, content_type = 'application/json')
    #return JsonResponse(serializer.data ,safe=false)
    
@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        users = Student.objects.all()
        print(users)
        serializer = StudentSerializers(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        new_data = {'name': request.POST.get('name'), 'email': request.POST.get('email')}
        print(new_data)
        serializer = StudentSerializers(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    