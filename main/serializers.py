from rest_framework import serializers
from .models import Drink, TouristicPlace, GeoInfo, Photo, Comment, Video

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

class TouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristicPlace
        fields = ['id', 'name', 'lat', 'long', 'description', 'category', 'nb_visitors', 'created_by', 'region', 'wilaya', 'ville']

class GeoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoInfo
        fields = ['id', 'wilaya', 'ville', 'region']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'touristicPlace']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video', 'touristicPlace']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'content', 'approved', 'rating', 'touristicPlace']


        