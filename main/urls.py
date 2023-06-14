from django.urls import path
from . import views

urlpatterns = [
    path('places/', views.TouristicPlacesView),
    path('geoinfo/', views.GeoInfoView),
    path('places/filter/', views.TouristicPlacesFitler.as_view()),
    path('places/photo/', views.PhotoViewSet.as_view({'post': 'create'})),
    path('places/<int:id>/', views.TouristicPlaceDetailsView), 
    path('comments/', views.CommentsView), 
    path('comments/<int:id>/', views.CommentsDetailsView)
]

