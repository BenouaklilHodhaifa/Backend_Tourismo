from rest_framework import serializers
from .models import *

# for authentication 
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model 
user = get_user_model()


class UserCreateSerializer(UserCreateSerializer): 
    class Meta(UserCreateSerializer.Meta): 
        model = user
        fields = ('id', 'email', 'name', 'password', 'region')

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'email', 'name', 'region', 'is_superuser']





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
        
        # def to_representation(self, instance): # if the instance is an "Event" then add "date_debut" and "date_fin"
        #     if isinstance(instance, Event):
        #         return EventSerializer(instance).data
        #     return super().to_representation(instance)


class EventSerializer(serializers.ModelSerializer):
    class Meta: 
        model =  Event
        # fields = ['id','name', 'lat', 'long', 'description','category', 'nb_visitors', 'created_by', 'geoinfo', 'date_debut', 'date_fin']
        fields = TouristicPlaceSerializer.Meta.fields + ['date_debut', 'date_fin']


class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment
        fields = ['id', 'name', 'content', 'approved', 'rating', 'touristicPlace']


class PhotoSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Photo
        fields = ['id', 'image', 'touristicPlace']

class VideoSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Video
        fields = ['id', 'video', 'touristicPlace']
