from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



@api_view(['GET','POST'])
def DrinkList(request): 
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)

        #return JsonResponse({"drinks":serialize.data})
        return Response(serializer.data, status=status.HTTP_200_OK) #this one is better
    
    elif request.method == 'POST': 
        serializer = DrinkSerializer(data=request.data)
        
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        #return JsonResponse({"error": "check your arguments"}, status= status.HTTP_400_BAD_REQUEST)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])

def DrinkDetails(request, id):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        
        return Response(data= serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': 
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        drink.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','POST'])
def TouristicPlaceList(request): 
    if request.method == 'GET': 
        touristicplaces = TouristicPlace.objects.all()
        serializer = DrinkSerializer(touristicplaces, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST': 
        serializer = TouristicPlaceSerializer(data=request.data)
        
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)