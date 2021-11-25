from django.db import models
# from django.db.models.deletion import CASCADE
# dont know why cascade got imported
from django.contrib.auth.models import User
# Create your models here.

# Room is child of Topic
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# the topic can have multiple rooms
# while the room can only have one topic

class Room(models.Model):
    # user model in django
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # when delete topic -> not delete room -> set_NULL
    # when set null -> need allow null = True, make sure database will allow it
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # participants =
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        # '-' is descending order
        ordering = ['-update', '-create']

    def __str__(self):
        return self.name 




# want have more models
class Message(models.Model):
    # use django customize user model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # one to many relationship
    # CASCADE means that when delete Room, the child also cascade delete
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    # we only want first 50 chars
    def __str__(self):
        return self.body[0:50] 