from django.urls import path
from ..api import views

urlpatterns = [
    # api version 1.
    path('v1/posts', views.posts_list),
    path('v1/posts/<int:pk>', views.post_detail),
    
    # api version 2
    path('v2/posts', views.posts_list_v2),
    path('v2/posts/<int:pk>', views.post_detail_v2),
]


