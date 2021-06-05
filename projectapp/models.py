from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.query import prefetch_related_objects

class Users(models.Model):
    first_name= models.CharField(max_length=45)
    last_name = models.CharField(max_length=45) 
    email = models.EmailField(max_length=2252)
    password = models.CharField(max_length=45) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Event(models.Model):
#     title= models.CharField(max_length=45)
#     date = models.CharField(max_length=45)
#     event=models.ManyToManyField(Users,related_name="events")
#     event_creator = models.ForeignKey(Users,related_name="created_event" , on_delete=models.CASCADE) 
#     description = models.CharField(max_length=2252)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)