from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import User


class Idea(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    likes = models.ManyToManyField(User, related_name='ideas_liked', blank=True)
    dislikes = models.ManyToManyField(User, related_name='ideas_disliked', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()


class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name='comments_liked', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comments_disliked', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s comment on '{self.idea.title}'"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()