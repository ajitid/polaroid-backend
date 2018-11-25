from rest_framework import decorators, views, mixins, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404
from django.db.models import F
from . import models, serializers


class UserCreateView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    permission_classes = []


# TODO change photo from a different url
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "username"

    def check_permissions(self, request):
        if (request.method in ("PUT", "PATCH", "DELETE")) and (self.kwargs["username"] != request.user.username):
            # TODO make sure Swagger or other doc generation doesn't skip methods mentioned in above condition
            raise MethodNotAllowed(request.method)
        return super().check_permissions(request)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()
    lookup_field = "user__username"
    lookup_url_kwarg = "username"

    def check_permissions(self, request):
        if (request.method in ("PUT", "PATCH")) and (self.kwargs["username"] != request.user.username):
            # TODO make sure Swagger or other doc generation doesn't skip methods mentioned in above condition
            raise MethodNotAllowed(request.method)
        return super().check_permissions(request)


class FollowersListView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        user = get_object_or_404(models.Profile, user__username=username)
        return user.followers.all().values("username", "name")


class FollowingListView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        user = get_object_or_404(models.Profile, user__username=username)
        return user.following.all().values("username", "name")
        # return queryset.values("user__name", "user__username").annotate(
        #     name=F("user__name"), username=F("user__username")
        # )


class Follow(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, username):
        user = get_object_or_404(models.User, username=username)
        return user

    def get(self, request, username):
        user = self.get_object(username)
        try:
            user.followers.get(user=request.user)
            return Response({"follows": True})
        except models.Profile.DoesNotExist:
            return Response({"follows": False})

    def post(self, request, username):
        user = self.get_object(username)
        if user == request.user:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user.profile.followers.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, username):
        user = self.get_object(username)
        if user == request.user:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user.profile.followers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
