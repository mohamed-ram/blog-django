from django.db import models
from django.db.models.signals import pre_save

from utils.receivers import slug_pre_save_receiver


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


pre_save.connect(sender=Category, receiver=slug_pre_save_receiver)

