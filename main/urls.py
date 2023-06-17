from django.urls import path
from . import views

urlpatterns = [
    path('places/', views.TouristicPlacesView),
    path('geoinfo/', views.GeoInfoView),
    path('geoinfo/<int:id>/', views.GeoInfoDetailsView),
    path('places/filter/', views.TouristicPlacesFilteringView.as_view()),
    path('places/search/', views.TouristicPlaceSearchView.as_view()),
    path('places/photo/', views.PhotoViewSet.as_view({'post': 'create'})),
    path('places/<touristicPlace>/photo/', views.AllImagesDetailsView.as_view()),
    path('places/<touristicPlace>/photo/<id>/', views.SingleImageDetailsView.as_view()),
    path('places/video/', views.VideoUploadView.as_view()),
    path('places/<touristicPlace>/video/', views.AllVideosDetailsView.as_view()),
    path('places/<touristicPlace>/video/<id>/', views.SingleVideoDetailsView.as_view()),
    path('places/<int:id>/', views.TouristicPlaceDetailsView), 
    path('comments/', views.CommentsView), 
    path('comments/<int:id>/', views.CommentsDetailsView)
]