from django.contrib import admin
from .models import Post
from .forms import PostForm
from tags.admin import TagInline
from images.admin import ImageInline

class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline, TagInline]
    form = PostForm
    list_display = ['title', 'slug', 'state', 'approved', 'category', 'timestamp', 'updated']
    
    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)

