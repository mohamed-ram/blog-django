from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Rate


class RateInline(GenericTabularInline):
    model = Rate
    fields = ['value', 'comment', 'user']
    extra = 1


admin.site.register(Rate)

