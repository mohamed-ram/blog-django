from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg, Max, Min
from django.db.models.signals import pre_save

from images.models import Image
from tags.models import Tag
from ratings.models import Rate

from utils.models import Category
from utils.constants import PublishState
from utils.receivers import slug_pre_save_receiver, publish_state_pre_save_receiver


User = settings.AUTH_USER_MODEL

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(approved=True, state=PublishState.PUBLISHED)
    
    def draft(self):
        return self.filter(state=PublishState.DRAFT)
    
    def private(self):
        return self.filter(approved=True, state=PublishState.PRIVATE)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def draft(self):
        return self.get_queryset().draft()
    
    def private(self):
        return self.get_queryset().private()


class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    images = GenericRelation(Image, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    content = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    state = models.CharField(max_length=20, choices=PublishState.choices)
    approved = models.BooleanField(default=False)
    tags = GenericRelation(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    ratings = GenericRelation(Rate, on_delete=models.SET_NULL, null=True, blank=True)
    
    objects = PostManager()
    
        
    
    def get_rating_average(self):
        post = Post.objects.get(id=self.id)
        average = post.ratings.aggregate(average=Avg("value"))
        return average
    
    def get_rating_spread(self):
        post = Post.objects.get(id=self.id)
        spread = post.ratings.aggregate(max=Max("value"), min=Min("value"))
        return spread
    
     
    def __str__(self):
        return self.title


pre_save.connect(sender=Post, receiver=slug_pre_save_receiver)
pre_save.connect(sender=Post, receiver=publish_state_pre_save_receiver)


class FeaturedPosts(Post):
    class Meta:
        proxy = True

