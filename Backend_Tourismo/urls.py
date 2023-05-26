from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drinks/', views.DrinkList),
    path('drinks/<int:id>/', views.DrinkDetails),
    # this is for authentication
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('lieux/',views.TouristicPlaceList )
]
