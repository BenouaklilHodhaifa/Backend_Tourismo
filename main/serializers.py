from rest_framework import serializers
from .models import Drink

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