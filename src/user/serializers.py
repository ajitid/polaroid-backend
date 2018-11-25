from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    # photo = serializers.ImageField(source="profile.photo")

    class Meta:
        model = models.User
        # small photo FIXME
        fields = ("username", "name")


class UserCreateSerializer(serializers.ModelSerializer):
    # putting password into extra kwargs doesn't work, maybe coz a non-model field
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    class Meta:
        model = models.User
        # small photo FIXME
        fields = ("username", "name", "email", "password")

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    name = serializers.ReadOnlyField(source="user.name")
    followers_count = serializers.ReadOnlyField(source="followers.count")
    following_count = serializers.ReadOnlyField(source="following.count")

    # Profile.objects.filter(followers__username="abhay")
    # TODO

    class Meta:
        model = models.Profile
        fields = ("username", "name", "photo", "dob", "bio", "followers_count", "following_count")
        extra_kwargs = {"photo": {"read_only": True}}


# delete account using /api/users/<username> with ["request"].user.username being same as username
# else forbidden (403) or 400 Bad Request
# forbidden if trying to follow youself or blocking
# likes own post by default (but no notif send)
