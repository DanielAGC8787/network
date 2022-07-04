from pyexpat import model
from signal import default_int_handler
from statistics import mode
from venv import create
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    # def serialize(self):
    #     return{
    #         "id": self.id,
    #         "username": self.username,
    #         "followers": self.followers
    #     }

class Following(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    following = models.CharField(max_length=64)
    # def serialize(self):
    #     return{
    #         "owner": self.owner.username,
    #         "follower": self.following
    #     }
    def __str__(self):
        return self.following
    
    def serialize(self):
        return{
            "id": self.id,
            "owner": self.owner.username,
            "following": self.following
        }

class Follower(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.CharField(max_length=64)
    # def serialize(self):
    #     return{
    #         "owner": self.owner.username,
    #         "follower": self.follower
    #     }
    def __str__(self):
        return self.follower

    def serialize(self):
        return{
            "id": self.id,
            "owner": self.owner.username,
            "following": self.follower
        }

class Post(models.Model):
    body = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timeStamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    liked = models.BooleanField(default=False)

    def serialize(self):
        return{
            "id": self.id,
            "creator": self.creator.username,
            "body": self.body,
            "timeStamp": self.timeStamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "liked": self.liked
        }

