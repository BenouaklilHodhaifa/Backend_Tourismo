from .models import Drink
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from .utils import send_newsletter_email # for newsletter
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

@api_view(['POST'])
def createEvent(request): 
    serializer = EventSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET', 'PUT', 'DELETE'])
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


class TouristicPlacesFitler(ListAPIView):
    queryset = TouristicPlace.objects.all()
    serializer_class = TouristicPlaceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['category', 'geoinfo__wilaya', 'geoinfo__ville', 'geoinfo__region'] 
    filters_fields = ['category', 'geoinfo__wilaya', 'geoinfo__ville', 'geoinfo__region']
    search_fields = ['category', 'geoinfo__wilaya', 'geoinfo__ville', 'geoinfo__region']
    #serializer = TouristicPlaceSerializer(queryset, many=True)
    #return JsonResponse(serializer.data, safe=False)

class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly]

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
            serializer.save(is_superuser=True)
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
    
    average = sum(rating_list)/len(rating_list)
    data = {
        "id": id,
        "rating_average": average, 
        "nb_visitors": touristicPlace.nb_visitors
    }
    return Response(data=data ,status=status.HTTP_200_OK) 

@api_view(['GET'])
def send_newsletter(request):
    #subscribers = NewsletterSubscriber.objects.all()
    subject = 'Newsletter Notification'
    message = 'Hello! This is a notification from our newsletter.'
    #recipient_list = [subscriber.email for subscriber in subscribers]
    recipient_list = ['ka_seddiki@esi.dz']
    send_newsletter_email(subject, message, recipient_list)
    return Response('Newsletter sent!', status=200)

