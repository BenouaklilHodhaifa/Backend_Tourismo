from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager #for the costum user model
from django.core.validators import MinValueValidator, MaxValueValidator # to validate the attribute "region" in "UserAccount" model
from .validators import file_size

class Drink(models.Model): # this is just a test
    name = models.CharField(max_length=200)
    description = models.TextField()

class UserAccountManager(BaseUserManager): 
    def create_user(self, email, name, password=None, is_superuser=False, region=None): 
        if not email:
            raise ValueError('user must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password) #hash the password
        user.is_superuser = is_superuser
        user.region = region 
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin): 
    
    email = models.EmailField(max_length=254, unique=True) #this is our login field
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    region = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'is_superuser', 'region']

    objects = UserAccountManager()

    def get_full_name(self): 
        return self.name
    
    def get_short_name(self): 
        return self.name
    
    def __str__(self):
        return self.email



class TouristicPlace(models.Model): 
    x= [ 
        ("beach", "beach"), 
        ("forrest", "forrest"),
        ("museum", "museum"), 
        ("monumant", "monumant"), 
        ("landmark", "landmark"), 
        ("public square", "public square"), 
        ("archaeological site", "archaeological site"), 
        ("garden", "garden"), 
        ("relegious site", "relegious site"), 
        ("market", "market"), 
        ("restaurant", "restaurant"), 
        ("event", "event")
    ]

    TRANSPORT_CHOICES = [
    ("car", "Car"),
    ("bus", "Bus"),
    ("train", "Train"),
    ("metro", "Metro"),
    ("walking", "Walking"),
    ("bicycle", "Bicycle"),
    ("motorcycle", "Motorcycle"),
    ("boat", "Boat"),
    ("ferry", "Ferry"),
    ("taxi", "Taxi"),
    ("ride-sharing", "Ride-sharing"),
    ("helicopter", "Helicopter"),
    ]

    name = models.CharField(max_length=60)
    lat = models.FloatField()
    long = models.FloatField()
    description = models.TextField()
    category = models.CharField( max_length=30, choices=x)
    nb_visitors =models.IntegerField(default=0) # for statistics
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True) #for the events
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES, null=True) # new for Transport
    created_by = models.ForeignKey(UserAccount, related_name="TouristicPlaces", on_delete=models.SET_NULL, null=True)
    region = models.CharField(max_length=50, null=True)
    wilaya = models.CharField( max_length=50, null=True)
    ville = models.CharField( max_length=50, null=True)




class Comment(models.Model): 
    name = models.CharField(max_length=50)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    rating = models.IntegerField()
    touristicPlace = models.ForeignKey(TouristicPlace, on_delete=models.CASCADE, null=True)

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Photo(models.Model):
    image = models.FileField(upload_to="multimedia", null=True, blank=True)
    touristicPlace = models.ForeignKey(TouristicPlace, on_delete=models.CASCADE, null=True)

class Video(models.Model): 
    video = models.FileField(upload_to="videos/", null=True, blank=True, validators=[file_size])
    touristicPlace = models.ForeignKey(TouristicPlace, on_delete=models.CASCADE, null=True)


class SubscriberVille(models.Model): 
    email = models.EmailField(max_length=254)
    ville = models.TextField(max_length=50)

class SubscriberRegion(models.Model): 
    email = models.EmailField(max_length=254)
    region = models.TextField(max_length=50)

    
