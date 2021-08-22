from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Post

def all_posts(request, query=None):
    posts = Post.objects.published()
    query = request.GET.get("q")
    
    if query:
        posts = Post.objects.published().filter(
                Q(title__contains=query) |
                Q(content__contains=query) |
                Q(category__title__contains=query)
            )
    count = posts.count()
    
    context = {"posts": posts,
               "count": count,
               "query": query,
               }
    return render(request, "posts/posts.html", context=context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {"post": post}
    return render(request, "posts/post_detail.html", context=context)