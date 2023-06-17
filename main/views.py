from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer, TouristicPlaceSerializer, GeoInfoSerializer, PhotoSerializer, CommentSerializer, VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .custom_renderers import PNGRenderer
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models import Q
import json

#from rest_framework import permissions

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
# @permissions_classes([IsAuthenticated])
def TouristicPlacesView(request):
    if request.method == 'GET':
        touristicPlaces = TouristicPlace.objects.all()
        serializer = TouristicPlaceSerializer(touristicPlaces, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)       

    elif request.method == 'POST':
        serializer = TouristicPlaceSerializer(data=request.data)

        print(request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])

def TouristicPlaceDetailsView(request, id):
    try:
        touristicPlace = TouristicPlace.objects.get(pk=id)        
    except TouristicPlace.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TouristicPlaceSerializer(touristicPlace)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': 
        serializer = TouristicPlaceSerializer(touristicPlace, data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        touristicPlace.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])

def CommentsView(request): 
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST': 
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])

def CommentsDetailsView(request, id):
    try:
        comment = Comment.objects.get(pk=id)        
    except Comment.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': 
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        comment.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)     

#will be deleted
@api_view(['GET','POST'])
#@permission_classes((IsAuthenticated, ))
def GeoInfoView(request):
    if request.method == 'GET':
        geoInfo = GeoInfo.objects.all()
        serializer = GeoInfoSerializer(geoInfo, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)       

    if request.method == 'POST':
        serializer = GeoInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
            
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def GeoInfoDetailsView(request, id):
    try:
        geoinfo = GeoInfo.objects.get(pk=id)        
    except GeoInfo.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GeoInfoSerializer(geoinfo)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': 
        serializer = GeoInfoSerializer(geoinfo, data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        geoinfo.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)     


class TouristicPlacesFilteringView(generics.ListAPIView):
    serializer_class = TouristicPlaceSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')
        theme = self.request.query_params.get('theme')
        queryset = TouristicPlace.objects.all()

        if category:
            queryset = queryset.filter(category=category)

        if theme:
            if theme == 'history and heritage':
                queryset = queryset.filter(category__in=['monumant','archaeological site'])

            elif theme == 'arts and culture':
                queryset = queryset.filter(category__in=['musee','landmark', 'archaeological site'])

            elif theme == 'nature and landscapes':
                queryset = queryset.filter(category__in=['beach','forest'])

            elif theme == 'spirituality and relegion':
                queryset = queryset.filter(category__in=['religious site', 'landscape'])
            
            elif theme == 'entertainment and leisure':
                queryset = queryset.filter(category__in=['event'])

            elif theme == 'gardens and green spaces':
                queryset = queryset.filter(category__in=['garden'])
            
            elif theme == 'Markets and shopping':
                queryset = queryset.filter(category__in=['market'])

            elif theme == 'gastronomy and cooking':
                queryset = queryset.filter(category__in=['restaurant'])

            elif theme == 'adventures and sports':
                queryset = queryset.filter(category__in=['beach','forest', 'public space'])

            elif theme == 'education and learning':
                queryset = queryset.filter(category__in=['musee','event'])

        return queryset


class TouristicPlaceSearchView(generics.ListAPIView):
    serializer_class = TouristicPlaceSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('query')
        queryset = TouristicPlace.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(category__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(region__icontains=search_query) |
                Q(wilaya__icontains=search_query) |
                Q(ville__icontains=search_query)
            )
            
        return queryset


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save()


class SingleImageDetailsView(generics.RetrieveAPIView):
    rendered_classes = [PNGRenderer]
    def get(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(touristicPlace_id=int(self.kwargs['touristicPlace']))[int(self.kwargs['id'])-1]
        path_image = queryset.image
        response = {
            "id": queryset.id,
            "image": "/media/"+str(path_image),
            "touristicPlace": queryset.touristicPlace.id
        }
        return Response(response, status=status.HTTP_200_OK)


class AllImagesDetailsView(generics.RetrieveAPIView):
    rendered_classes = [PNGRenderer]
    def get(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(touristicPlace_id=int(self.kwargs['touristicPlace']))#[int(self.kwargs['id'])-1].image
        print(queryset)
        serializer = PhotoSerializer(queryset, many=True)
        print(serializer.data)
        tab = []
        json_data = {}
        i = 0
        for obj in serializer.data:
            for key, value in obj.items():
                json_data[key] = value
            tab.append(json_data)
            i+=1
        json_response = tab
        return Response(json_response, status=status.HTTP_200_OK)


class VideoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleVideoDetailsView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Video.objects.filter(touristicPlace_id=int(self.kwargs['touristicPlace']))[int(self.kwargs['id'])-1]
        path_video = queryset.video
        response = {
            "id": queryset.id,
            "video": "/media/"+str(path_video),
            "touristicPlace": queryset.touristicPlace.id}
        return Response(response, status=status.HTTP_200_OK)


class AllVideosDetailsView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Video.objects.filter(touristicPlace_id=int(self.kwargs['touristicPlace']))#[int(self.kwargs['id'])-1].image
        print(queryset)
        serializer = VideoSerializer(queryset, many=True)
        print(serializer.data)
        tab = []
        json_data = {}
        i = 0
        for obj in serializer.data:
            for key, value in obj.items():
                json_data[key] = value
            tab.append(json_data)
            i+=1
        json_response = tab
        return Response(json_response, status=status.HTTP_200_OK)
