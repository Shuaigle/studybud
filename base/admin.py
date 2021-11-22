from django.contrib import admin

# Register your models here.

# want to see Room model in admin
# when update migrate models, need to add in admin
from .models import Room, Topic, Message

# register admin panel with Room and Room will appear at admin page
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
# than create some instances in admin Room model
# we want to see those instances in main pages
# need to use views.py