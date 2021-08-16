from django.contrib.auth.models import User, Group
from django.http import JsonResponse, Http404
from rest_framework import viewsets, generics
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer, GroupSerializer, PostsSerializer, CommentsSerializer
from .models import Comments, Posts


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

#
# class PostsViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Posts.objects.all().order_by('-id')
#     serializer_class = PostsSerializer
#     permission_classes = [permissions.IsAuthenticated]


class ListPosts(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request):
        """
        Return a list of all users.
        """
        posts_all = Posts.objects.all()
        posts = PostsSerializer(posts_all, many=True)
        return Response(posts.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class PostsDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PostsSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PostsSerializer(snippet, data=request.data, context={'request': request})
        if serializer.is_valid() and self.request.user == snippet.author:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if self.request.user == snippet.author:
            snippet.delete()
            return Response(status=204)
        return Response(status=400)


class CommentsDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CommentsSerializer(snippet, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CommentsSerializer(snippet, data=request.data, context={'request': request})
        if serializer.is_valid() and self.request.user == snippet.author:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if self.request.user == snippet.author:
            snippet.delete()
            return Response(status=204)
        return Response(status=400)
