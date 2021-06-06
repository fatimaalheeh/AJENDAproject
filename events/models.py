from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.query import prefetch_related_objects

class EventManager(models.Manager):
    def event_validator(self, postData):
        errors = {}
        if len(postData['description']) < 5:
            errors['description'] = "you must type over 5 characters for your description!"
        if len(postData['description']) < 1:
            errors['description'] = "Please provide event!" 
        return errors 

class Users(models.Model):
    first_name= models.CharField(max_length=45)
    last_name = models.CharField(max_length=45) 
    email = models.EmailField(max_length=2252)
    password = models.CharField(max_length=45) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #created_event/ list/ 1-m
    #attende_events / attended/ list/ m-m
    objects = EventManager() #manager for validating event
class Event(models.Model):
    title= models.CharField(max_length=45, default='title')
    date = models.CharField(max_length=45, default='2012-06-06')
    attended_by=models.ManyToManyField(Users,related_name="attended_events")
    event_creator = models.ForeignKey(Users,related_name="created_event" , on_delete=models.CASCADE) 
    description = models.CharField(max_length=2252, default='description')
    objects=EventManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def total_attended(self):
        return self.attended.count()
