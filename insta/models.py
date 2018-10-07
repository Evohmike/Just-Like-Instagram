from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  Name = models.TextField(default="Mike")
  profile_picture = models.ImageField(upload_to='users/', default='users/user.png')
  bio = models.TextField(default="I love instagram!")

  def save_profile(self):
      self.save()
  
  @classmethod
  def search_profile(cls, name):
      profile = Profile.objects.filter(user__username__icontains = name)
      return profile
  
  @classmethod
  def get_by_id(cls, id):
      profile = Profile.objects.get(user = id)
      return profile

  @classmethod
  def filter_by_id(cls, id):
      profile = Profile.objects.filter(user = id).first()
      return profile



class Post(models.Model):
  image = models.ImageField(upload_to='posts/')
  user = models.ForeignKey(Profile, related_name='posts')



