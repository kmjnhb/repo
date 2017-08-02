from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


admin.site.register(Client)