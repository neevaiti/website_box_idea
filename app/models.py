from django.contrib.auth.models import User
from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes_count = models.IntegerField(blank=True, default=0)
    dislikes_count = models.IntegerField(blank=True ,default=0)


class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.IntegerField(blank=True, default=0)
    dislikes = models.IntegerField(blank=True, default=0)