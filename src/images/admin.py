from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Image

class ImageInline(GenericTabularInline):
    model = Image
    fields = ['image', 'title', 'order']
    extra = 0


admin.site.register(Image)

