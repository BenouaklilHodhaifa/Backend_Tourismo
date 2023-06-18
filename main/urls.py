from django.urls import path
from . import views

urlpatterns = [
    path('places/', views.TouristicPlacesView),
    path('places/filter/', views.TouristicPlacesFilteringView.as_view()),
    path('places/search/', views.TouristicPlaceSearchView.as_view()),
    path('places/photo/', views.PhotoViewSet.as_view({'post': 'create'})),
    path('places/<touristicPlace>/photo/', views.AllImagesDetailsView.as_view()),
    path('places/<touristicPlace>/photo/<id>/', views.SingleImageDetailsView.as_view()),
    path('places/video/', views.VideoUploadView.as_view()),
    path('places/<touristicPlace>/video/', views.AllVideosDetailsView.as_view()),
    path('places/<touristicPlace>/video/<id>/', views.SingleVideoDetailsView.as_view()),
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
    path("newsletter/region/<int:id>/delete/", views.DeleteSubscriberRegion),
    path("newsletter/ville/<int:id>/delete/", views.DeleteSubscriberVille)
]
