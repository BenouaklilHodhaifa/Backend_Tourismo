from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager #for the costum user model
from django.core.validators import MinValueValidator, MaxValueValidator # to validate the attribute "region" in "UserAccount" model


class Drink(models.Model): # this is just a test
    name = models.CharField(max_length=200)
    description = models.TextField()

class UserAccountManager(BaseUserManager): 
    def create_user(self, email, name, password=None): 
        if not email:
            raise ValueError('user must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password) #hash the password 
        user.save()

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('superuser must have an email adresse')

        email = self.normalize_email(email)
        superuser = self.model(email=email, **extra_fields)
        superuser.set_password(password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()

        return superuser


class UserAccount(AbstractBaseUser, PermissionsMixin): 
    
    email = models.EmailField(max_length=254, unique=True) #this is our login field
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    region = models.IntegerField( # every wilaya is a region
        validators=[
            MinValueValidator(1),
            MaxValueValidator(58)
        ], null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserAccountManager()

    def get_full_name(self): 
        return self.name
    
    def get_short_name(self): 
        return self.name
    
    def __str__(self):
        return self.email


class GeoInfo(models.Model): 
        wilaya = models.CharField( max_length=50)
        ville = models.CharField( max_length=50)
        region = models.CharField(max_length=50)

class TouristicPlace(models.Model): 
    x= [ # add the rest
        ("beach", "beach"), 
        ("museum", "museum"), 
        ("monumant", "monumant")
    ]

    name = models.CharField(max_length=60)
    lat = models.FloatField()
    long = models.FloatField()
    description = models.TextField()
    category = models.CharField( max_length=30, choices=x)
    nb_visitors =models.IntegerField(default=0) # for statistics
    created_by = models.ForeignKey(UserAccount, related_name="TouristicPlaces", on_delete=models.SET_NULL, null=True)
    geoinfo = models.ForeignKey(GeoInfo ,on_delete=models.CASCADE, null=True)

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
    video = models.FileField(upload_to="multimedia", null=True, blank=True)
    touristicPlace = models.ForeignKey(TouristicPlace, on_delete=models.CASCADE, null=True)



    