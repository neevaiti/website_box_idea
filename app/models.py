from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import User

class User(User):
    # champs supplémentaires pour stocker l'image de profil
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # autres champs de l'utilisateur
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username



class PostIdea(models.Model):
    """
    This class represents the model of the idea
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title