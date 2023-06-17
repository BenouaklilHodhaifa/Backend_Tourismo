from django.urls import path
from . import views

urlpatterns = [
    path('places/', views.TouristicPlacesView),
    # path('geoinfo/', views.GeoInfoView),
    # path('geoinfo/<int:id>/', views.GeoInfoDetailsView),
    path('places/filter/', views.TouristicPlacesFitler.as_view()),
    path('places/photo/', views.PhotoViewSet.as_view({'post': 'create'})),
    path('places/<int:id>/', views.TouristicPlaceDetailsView), 
    path("places/<int:id>/approvedcomments/", views.getApprovedComments),
    path('comments/', views.CommentsView), 
    path("comments/notapproved/", views.getAllNonApprovedComments),
    path('comments/<int:id>/', views.CommentsDetailsView), 
    path('comments/<int:id>/approved/', views.approvingComment),
    path('centraladmins/', views.SuperUserView), 
    path('centraladmins/<int:id>/', views.SuperUserDetailsView), 
    path('places/<int:id>/stats/', views.StatisicsView), 
    path("newsletter/region/", views.CreateSubscriberRegion), 
    path("newsletter/ville/", views.CreateSubscriberVille), 
    path("newsletter/region/<int:id>/", views.DeleteSubscriberRegion),
    path("newsletter/ville/<int:id>/", views.DeleteSubscriberVille), 
    path('email/region/', views.sendEmailsRegion), #for testing
    path('email/ville/', views.sendEmailsVille) #for testing
]

