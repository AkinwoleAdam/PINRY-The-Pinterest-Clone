from django.db import models
from django.contrib.auth.models import User
from mimetypes import guess_type

# Create your models here.

status = (('private','private'),('public','public'))

class Board(models.Model):
  user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
  title = models.CharField(max_length=200)
  description = models.TextField(null=True,blank=True)
  status = models.CharField(max_length=200,blank=True,null=True,choices=status,default='public')
  cover = models.ImageField(null=True,blank=True)
  date_created = models.DateTimeField(auto_now_add = True)
  date_updated = models.DateTimeField(auto_now = True)
  
  def __str__(self):
    return self.title
    
    
class Pin(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
  board = models.ForeignKey(Board,on_delete=models.SET_NULL,null=True,blank=True)
  name = models.CharField(max_length=250)
  description = models.TextField(null=True,blank=True)
  file = models.FileField()
  date_created = models.DateTimeField(auto_now_add = True)
  date_updated = models.DateTimeField(auto_now = True)
  
  def __str__(self):
    return self.name
    
  def get_type(self):
    file_type = guess_type(self.file.url, strict=True)[0]
    # file_type might be ('video/mp4', None) or ('image/jpeg..etc', None)
    if 'video' in file_type:
      return 'video'
    elif 'image' in file_type:
      return 'image'
  
  class Meta:
    ordering = ['-date_updated','-date_created']
    
class Comment(models.Model):
  user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  pin = models.ForeignKey(Pin,related_name='comments',on_delete=models.SET_NULL,null=True)
  body = models.TextField(null=True)
  date_created = models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering = ['-date_created']
    
  def __str__(self):
    return self.body    
    
    
class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  bio = models.TextField()
  avatar = models.ImageField(default='profile1.png',null=True)
  website_link = models.URLField(null=True,blank=True)
  
  def __str__(self):
    return f'{self.user.username} Profile'    