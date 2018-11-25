import os.path as path
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _, gettext
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from PIL.Image import LANCZOS


class User(AbstractUser):
    email = models.EmailField(_("email address"))
    first_name = None
    last_name = None
    name = models.CharField(_("name"), max_length=50)

    def get_short_name(self):
        if not self.name:
            return ""
        name_with_abbr = self.name[0 : self.name.rfind(".") + 1]
        if name_with_abbr:
            return name_with_abbr
        return self.name.split()[0]

    class Meta(AbstractUser.Meta):
        pass


def get_profile_photo_path(instance, filename):
    name, ext = path.splitext(filename)
    return path.join("profile-photo", f"{instance.user.username}{ext}")


class Profile(models.Model):
    # user not pk=True because of weird Django AUTH_PROFILE_SOMETHING and SQLite issue
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    photo = ProcessedImageField(
        upload_to=get_profile_photo_path,
        blank=True,
        processors=[ResizeToFit(width=240)],
        format="JPEG",
        options={"quality": 75, "optimize": True, "upscale": True, "filter": LANCZOS},
    )
    dob = models.DateField(_("date of birth"), blank=True, null=True)
    bio = models.CharField(max_length=180, blank=True)
    followers = models.ManyToManyField(User, related_name="followers", symmetrical=False, blank=True)
    blocked_users = models.ManyToManyField(User, related_name="blocked_users", symmetrical=False, blank=True)

    @property
    def following(self):
        return User.objects.filter(profile__followers__username=self.user.username)

    def __str__(self):
        return f"{self.user.username}"


# FIXME profile.photo
