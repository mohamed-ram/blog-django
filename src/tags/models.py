from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save

from utils.receivers import slug_pre_save_receiver


class Tag(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    def __str__(self):
        return self.title


pre_save.connect(sender=Tag, receiver=slug_pre_save_receiver)
