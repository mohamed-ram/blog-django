from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Tag

class TagInline(GenericTabularInline):
    model = Tag
    fields = ['title']
    extra = 1

