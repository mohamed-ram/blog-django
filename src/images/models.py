from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


def upload_to(instance, image_name):
    extension = image_name.split(".")[-1]
    return f"images/{instance.title}.{extension}"


class Image(models.Model):
    image = models.ImageField(upload_to=upload_to)
    title = models.CharField(max_length=60, blank=True, null=True)
    order = models.IntegerField(default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    
    def __str__(self):
        return F"{self.title} image."
    
    class Meta:
        ordering = ['order']

