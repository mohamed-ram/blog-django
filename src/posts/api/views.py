from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status

from posts.models import Post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import PostCreateUpdateSerializer, PostSerializer


# version 1 of posts api..
# posts list..
@csrf_exempt
def posts_list(request):
    posts = Post.objects.published()
    
    # get posts list.
    if request.method == 'GET':
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    # create new post.
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.author = request.user.id
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post detail..
@csrf_exempt
def post_detail(request, pk):
    try:
        post = Post.objects.published().get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    # GET..
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    
    # PUT..
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostCreateUpdateSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # DELETE..
    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)


# version 2 of posts api..[api_view()]
@api_view(['GET', 'POST'])
def posts_list_v2(request):
    # GET
    if request.method == 'GET':
        posts = Post.objects.published()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    # POST
    elif request.method == 'POST':
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def post_detail_v2(request, pk):
    try:
        post = Post.objects.published().get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET..
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # PUT..
    elif request.method == "PUT":
        serializer = PostCreateUpdateSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE..
    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)