from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from .validators import validate_file

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_client = models.BooleanField(default = False)
    city = models.CharField(max_length=20,blank=True)
    university = models.CharField(max_length=100, blank=True)
    dormitory = models.CharField(max_length=100, blank=True)
    room = models.CharField(max_length=15,blank=True)
    phonenumber = models.CharField(max_length=11,blank=True)

    @receiver(post_save, sender=User)
    def create_user_client(sender, instance, created, **kwargs):
    	if created:
    		client =Client(user=instance)
    		client.save()

    @receiver(post_save, sender=User)
    def save_user_client(sender, instance, **kwargs):
    	instance.client.save()
 


class Manager(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	is_manager = models.BooleanField(default = False)



class Printing(models.Model):
    user = models.ForeignKey(Client)
    file = models.FileField(validators=[validate_file])
    date=models.DateTimeField(auto_now_add=True)
    num_pages=models.IntegerField( )
    is_colored = models.BooleanField(default=False) # является ли печать цветной
    with_clip = models.BooleanField(default=False)  # идет ли в комплект скрепка
    with_clamp = models.BooleanField(default=False) #идет ли в комплект захим степлером



admin.site.register(Client)
admin.site.register(Printing)      
  


