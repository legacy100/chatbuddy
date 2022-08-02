from django.db import models
from django.contrib.auth.models import AbstractUser
# from sqlalchemy import null


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

# NOTE: Here a topic can have multiple rooms but a room can only have one topic.
# if the Topic class was set below the Room class, then the Topic attribute will be inputed in the Room class like this : 'Topic'

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
# we need to use a related name atrribute in order to run a proper many to many relationship because we already have the User in the host var.
    participants = models.ManyToManyField(User, related_name="participants", blank=True) 
# auto_now=True takes a snapshot of the timestamp when an update is made in the db
    updated = models.DateTimeField(auto_now=True)
#auto_now_add=True takes a snapshot of the timstamp when the data is actually created and it dosent change unlike "auto_now=True"
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated','-created']

# create a string representation of the Room class
    def __str__(self):
        return self.name



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body= models.TextField()
    updated= models.DateTimeField(auto_now=True)
    created= models.DateTimeField(auto_now_add=True)
    # ordering = ['-updated','-created']


    def __str__(self):
        return self.body[0:30]