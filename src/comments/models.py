from django.conf import settings
from django.db import models

from posts.models import Post


User = settings.AUTH_USER_MODEL



class CommentQuerySet(models.QuerySet):
    def parents(self):
        return self.filter(parent__isnull=True)
    

class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)
    
    def parents(self):
        return self.get_queryset().parents()
    

class Comment(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               null=True, blank=True, related_name="replies")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, max_length=400)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = CommentManager()
    
    def __str__(self):
        return self.content

