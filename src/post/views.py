from rest_framework import status, decorators, views, mixins, viewsets, response, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404

# from django.db.models import F

from . import models, serializers


class PostCreateView(generics.CreateAPIView):
    serializer_class = serializers.PostWithUrlSerializer
    queryset = models.Post.objects.all()
    permission_classes = (IsAuthenticated,)


class PostView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostWithPhotoReadOnlySerializer
    lookup_field = "id"

    # def get_serializer_class(self):
    #     serializer_class = self.serializer_class
    #     if self.request.method in ("PUT", "PATCH"):
    #         serializer_class = serializers.PostWithPhotoReadOnlySerializer
    #     return serializer_class

    def check_permissions(self, request):
        if request.method in ("PUT", "PATCH", "DELETE"):
            # TODO make sure Swagger or other doc generation doesn't skip methods mentioned in above condition
            post = get_object_or_404(models.Post, id=self.kwargs["id"])
            if post.user != request.user:
                raise MethodNotAllowed(request.method)
        return super().check_permissions(request)


class UserPostListView(generics.ListAPIView):
    serializer_class = serializers.PostThumbnailOnlySerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        user = get_object_or_404(models.User, username=username)
        queryset = user.posts.all()
        return queryset


class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostCommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(models.Post, id=post_id)
        queryset = post.comments.all()
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs["post_id"]
        if self.kwargs.get("pk") is not None:
            context["id"] = self.kwargs["pk"]
        return context

    def check_permissions(self, request):
        if request.method in ("PUT", "PATCH", "DELETE"):
            # TODO make sure Swagger or other doc generation doesn't skip methods mentioned in above condition
            comment = get_object_or_404(models.Comment, pk=self.kwargs["pk"], post__id=self.kwargs["post_id"])
            if comment.user != request.user:
                raise MethodNotAllowed(request.method)
        return super().check_permissions(request)

    # TODO didn't needed to define `check_permissions` like above, check why


class PostLikeView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        post = get_object_or_404(models.Post, id=id)
        return post

    def post(self, request, id):
        post = self.get_object(id)
        post.likes.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, id):
        post = self.get_object(id)
        post.likes.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedView(generics.ListAPIView):
    serializer_class = serializers.PostWithUrlSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = self.request.user.username
        queryset = models.Post.objects.filter(user__profile__followers__username=username)
        return queryset
