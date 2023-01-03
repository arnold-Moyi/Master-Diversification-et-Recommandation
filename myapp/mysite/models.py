from multiprocessing.spawn import import_main_path
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Lieu(models.Model):
    genres_choices = (
        ("restaurant", "Restaurant"),
        ("hotel", "Hotel"),
        ("cinema", "Cinema"),
        ("parc", "Parc"),
        ("plage", "Plage"),
        ("centre Commercial", "Centre Commercial"),
        ("jardin", "Jardin"),
        ("centre culturel", "Centre Culturel"),
        ("bibliotheque", "Bibliothèque"),
        ("théatre", "Théatre"),
        ("musée", "Musée"), 
        
    )
    name_place = models.CharField(max_length=255)
    categories = models.CharField(max_length=255, choices=genres_choices, blank=False, null=False)
    adress = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    image =models.ImageField(upload_to = "lieu_image")
    
    def __str__(self) :
        return str(self.pk)

class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  default=None)
    preference = models.CharField(max_length=254)
    
    def __str__(self):
        return self.preference

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, default= None)
    rating =models.CharField(max_length=100)
    rated_date = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.rating
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=500)
    
    def __str__(self):
        return self.name   


    