from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone
import random
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default = 'Default Name',max_length=30)
    areaOfInterest = models.CharField("Area of Interest",default='CSE',max_length=100)
    image= models.ImageField(default = 'default.jpg', upload_to='profile_pic')
    flag = models.BooleanField(default=False)
    varifiedProfile = models.BooleanField(default=False)
    OTP = models.IntegerField(default=random.randint(100000,999999))
    phoneNumber = models.IntegerField("Phone Number",blank=True,default=1212121212)
    githubHandle = models.CharField("Github Profile",max_length=100,blank=True)
    linkedinHandle = models.CharField("LinkedIn Profile",max_length=150,blank=True)
    portfolio = models.CharField("Portfolio",max_length=150,blank=True)
    facebookHandle = models.CharField("Facebook Profile",max_length=150,blank=True)
    
    def __str__(self):
        return str(self.user.username)+' Profile'
    
    def save(self,*args,**kwargs):
       super().save() 
       img = Image.open(self.image.path)
       if img.height>300 or img.width>300:
           output_size = (300,300)
           img.thumbnail(output_size)
           img.save(self.image.path)

class MessageData(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    senderName = models.CharField(max_length=100,blank=False)
    recieverID = models.IntegerField(blank=False)
    messageText = models.CharField(max_length=1000,blank=False)
    timeStamp = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return 'Message - '+str(self.id)
    
    def get_absolute_url(self):
        return reverse('message')
    class Meta:
        verbose_name = "Messages"
        verbose_name_plural = "Messages"
class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notice = models.CharField(max_length=1000,blank=False)
    timeStamp = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username+"'s Notice"
    class Meta:
        verbose_name_plural = 'Notifications'
class Following(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    friends = models.ManyToManyField(Profile)

    def __str__(self):
        return str(self.user)+"'s following"
    
    class Meta:
        verbose_name= 'Following'
        verbose_name_plural= 'Following'

class Followers(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    friends = models.ManyToManyField(Profile)

    def __str__(self):
        return str(self.user)+"'s followers"
    
    class Meta:
        verbose_name= 'Followers'
        verbose_name_plural= 'Followers'