from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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

  @classmethod
  def find_profile(cls,name):
      return cls.objects.filter(user__username__icontains = name).all()



class Post(models.Model):
  image = models.ImageField(upload_to='posts/')
  user = models.ForeignKey(Profile, related_name='posts')

  @classmethod
  def get_user_img(cls, id):
      return cls.objects.filter(user__id=id)


class Comment(models.Model):
    user= models.ForeignKey(User)
    post=models.ForeignKey('Post',null=True)
    comment= models.CharField(max_length=100)
    posted_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    # class Meta:
    #     ordering = ['-']

