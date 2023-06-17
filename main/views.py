from .serializers import *
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
from rest_framework.generics import ListAPIView

from .utils import * # for newsletter
from .custom_renderers import PNGRenderer
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models import Q
import json


@api_view(['GET','POST'])
# @permissions_classes([IsAuthenticated])
def TouristicPlacesView(request):
    if request.method == 'GET':
        touristicPlaces = TouristicPlace.objects.all()
        serializer = TouristicPlaceSerializer(touristicPlaces, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)       

    elif request.method == 'POST':
        serializer = TouristicPlaceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            if serializer.data["category"] == 'event':
                send_newsletter_region(region=serializer.data["region"], event_name=serializer.data["name"] ,
                                       date=serializer.data["date_debut"] ,description=serializer.data["description"] )
                send_newsletter_ville(ville=serializer.data["ville"], event_name=serializer.data["name"] ,
                                      date=serializer.data["date_debut"] ,description=serializer.data["description"])
            return Response(serializer.data, status= status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])

def TouristicPlaceDetailsView(request, id):
    try:
        touristicPlace = TouristicPlace.objects.get(pk=id)        
    except TouristicPlace.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        touristicPlace.nb_visitors += 1 # nb_vistors++ for stats
        touristicPlace.save()
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

@api_view(['PUT'])
def approvingComment(request, id):
    try:
        comment = Comment.objects.get(pk=id)        
    except Comment.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    comment.approved = True
    comment.save()

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getApprovedComments(request, id):
    "get approved comments for a specific Touristic Place"
    try:
        touristicPlace = TouristicPlace.objects.get(pk=id)
    except TouristicPlace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    comments = touristicPlace.comment_set.filter(approved=True)
    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAllNonApprovedComments(request):
    comments = Comment.objects.filter(approved=False)
    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
    

class TouristicPlacesFitler(ListAPIView):
    queryset = TouristicPlace.objects.all()
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



@api_view(['GET', 'POST'])
def SuperUserView(request):
    if request.method == 'GET': 
        users = UserAccount.objects.all()
        serializer = UserAccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST': 
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_superuser=True, region="all")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def SuperUserDetailsView(request, id): 

    try:
        superuser = UserAccount.objects.get(pk=id)        
    except UserAccount.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': 
        serializer = UserAccountSerializer(superuser)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': 
        serializer = UserAccountSerializer(superuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE': 
        "Delete any admin"
        user = UserAccount.objects.get(pk=id) 
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def StatisicsView(request, id): 
    """GET the statistics about a specific Touristic Place
    (visitors number and the average appreciation given by users)"""
    try:
        touristicPlace = TouristicPlace.objects.get(pk=id)        
    except TouristicPlace.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    comments = touristicPlace.comment_set.all()
    rating_list = []
    for comment in comments:
        if comment.approved:
            rating_list.append(comment.rating)
    
    if len(rating_list) != 0:
        average = sum(rating_list)/len(rating_list)
        data = {
            "id": id,
            "rating_average": average, 
            "nb_visitors": touristicPlace.nb_visitors
        }
        return Response(data=data ,status=status.HTTP_200_OK) 
    
    data = {
        "error": "There is no approved comments for this Touristic Place"
    }

    return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST', 'GET'])
def CreateSubscriberRegion(request):
    if request.method == 'POST': 
        serializer = SubscriberRegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET': 
        subscribers = SubscriberRegion.objects.all()
        serializer = SubscriberRegionSerializer(subscribers, many=True)
        
        return Response(serializer.data)
        

@api_view(['POST', 'GET'])
def CreateSubscriberVille(request):
    if request.method == 'POST':
        serializer = SubscriberVilleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        subscribers = SubscriberVille.objects.all()
        serializer = SubscriberVilleSerializer(subscribers, many=True)
        
        return Response(serializer.data)

@api_view(['DELETE'])
def DeleteSubscriberRegion(request, id):
    try:
        subscriber = SubscriberRegion.objects.get(pk=id)
    except SubscriberRegion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    subscriber.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def DeleteSubscriberVille(request, id):
    try:
        subscriber = SubscriberVille.objects.get(pk=id)
    except SubscriberVille.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    subscriber.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)






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
