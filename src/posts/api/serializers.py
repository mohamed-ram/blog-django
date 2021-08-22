from rest_framework import serializers

from posts.models import Post
from utils.models import Category

from accounts.api.serializers import AuthorSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']



class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ["id", "title", "author", "slug", "image", "content",
                  "timestamp", "updated", "category", "state", "approved"]
        # depth = 1

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ["title", "image", "content", "category", "state"]

