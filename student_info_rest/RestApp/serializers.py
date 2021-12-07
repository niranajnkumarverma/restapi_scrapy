from rest_framework import serializers
class StudentSerializers(serializers.Serializer): 
 id = serializers.IntegerField()   
 name  = serializers.CharField(max_length=50)
 roll = serializers.IntegerField()
 city = serializers.CharField(max_length=50)
 state = serializers.CharField(max_length=50)


 