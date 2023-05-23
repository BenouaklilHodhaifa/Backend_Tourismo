from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager #for the costum user model


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


class UserAccount(AbstractBaseUser, PermissionsMixin): 
    
    email = models.EmailField(max_length=254, unique=True) #this is our login field
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserAccountManager()

    def get_full_name(self): 
        return self.name
    
    def get_short_name(self): 
        return self.name
    
    def __str__(self):
        return self.email