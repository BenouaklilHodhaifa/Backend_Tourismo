from rest_framework import serializers
from .models import *

# for authentication 
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model 
user = get_user_model()


class UserCreateSerializer(UserCreateSerializer): 
    class Meta(UserCreateSerializer.Meta): 
        model = user
        fields = ('id', 'email', 'name', 'password')





class DrinkSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Drink 
        fields = ['id', 'name', 'description']
    
class GeoInfoSerializer(serializers.ModelSerializer):
    class Meta: 
        model =  GeoInfo
        fields = ['id', 'wilaya', 'ville', 'region']


class TouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta: 
        model =  TouristicPlace
        fields = ['id','name', 'lat', 'long', 'description', 'category', 'nb_visitors', 'created_by', 'geoinfo']

class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment
        fields = ['id', 'name', 'content', 'approved', 'rating', 'touristicplace']


class PhotoSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Photo
        fields = ['id', 'image', 'touristicplace']

class VideoSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Video
        fields = ['id', 'video', 'touristicplace']
