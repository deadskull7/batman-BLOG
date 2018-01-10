from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import gettext as _

class Post(models.Model):
    author = models.ForeignKey(User,  on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    image = models.ImageField( default = 'media/Bugatti-Chiron.jpg')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date"]

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments' ,on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    class Meta:
        ordering = ["-created_date"]


class Contact(models.Model):
      name = models.CharField(max_length=50,blank=True)
      email = models.EmailField()  
      comment = models.CharField(max_length=10000)

      def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user',  on_delete=models.CASCADE)
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = UserProfile(user=user)
            user_profile.save()
    post_save.connect(create_profile, sender=User)




     