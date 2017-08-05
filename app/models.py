from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from .validators import validate_file

class University(models.Model):
    name = models.CharField(max_length = 100, blank = True)

    def __str__(self):
        return self.name



class FranchiseAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_fradmin = models.BooleanField(default = True)
    city = models.CharField(max_length=20,blank=True)
    university = models.ForeignKey(University,null=True)
    room = models.CharField(max_length=15,blank=True)
    phonenumber = models.CharField(max_length=11,blank=True)

    def save(self, *args, **kwargs):
        super(FranchiseAdmin, self).save(*args, **kwargs)
    




class Dormitory(models.Model):
    name = models.CharField(max_length=100, blank = True)
    #это связь скорее всего лишняя
    university = models.ForeignKey(University,null = True)
    fadmin = models.ForeignKey(FranchiseAdmin,null = True)

    def __str__(self):
        return self.name
    
    

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    is_client = models.BooleanField(default = True)
    city = models.CharField(max_length=20,blank=True)
    university = models.ForeignKey(University,null=True)
    dormitory = models.ForeignKey(Dormitory,null=True)
    room = models.CharField(max_length=15,blank=True)
    phonenumber = models.CharField(max_length=11,blank=True)


    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)
        



class Manager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    fradmin = models.ForeignKey(FranchiseAdmin,null=True)
    is_manager = models.BooleanField(default = True)
    dormitory = models.ForeignKey(Dormitory,null=True)

    def save(self, *args, **kwargs):
        super(Manager, self).save(*args, **kwargs)
	
    
	

#заказ на принт
class Printing(models.Model):
    client = models.ForeignKey(Client,null=True)
    manager = models.ForeignKey(Manager,null=True)
    file = models.FileField(validators=[validate_file],null=True)
    date=models.DateTimeField(auto_now_add=True)
    num_pages=models.IntegerField(default=0)
    is_colored = models.BooleanField(default=False) # является ли печать цветной
    with_clip = models.BooleanField(default=False)  # идет ли в комплект скрепка
    with_clamp = models.BooleanField(default=False) #идет ли в комплект зажим степлером



admin.site.register(FranchiseAdmin)
admin.site.register(Manager)
admin.site.register(Client)
admin.site.register(Printing)      
admin.site.register(University)  
admin.site.register(Dormitory)  

