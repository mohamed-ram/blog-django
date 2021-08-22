from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('posts/', views.all_posts),
    path('posts/<str:slug>', views.post_detail, name="post_detail"),
]

