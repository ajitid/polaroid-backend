from uuid import uuid4
import os.path as path
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _, gettext
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
from PIL.Image import LANCZOS

User = get_user_model()


def get_post_media_path(instance, filename):
    name, ext = path.splitext(filename)
    return path.join("post-media", f"{instance.id}{ext}")


class Post(models.Model):
    id = models.UUIDField(_("post id"), primary_key=True, default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    photo = ProcessedImageField(
        upload_to=get_post_media_path,
        processors=[ResizeToFit(width=640)],
        format="JPEG",
        options={"quality": 75, "optimize": True, "upscale": True, "progressive": True, "filter": LANCZOS},
    )
    thumbnail = ImageSpecField(
        source="photo", processors=[ResizeToFit(width=320)], format="JPEG", options={"quality": 60}
    )
    caption = models.CharField(max_length=180, blank=True)
    timestamp = models.DateTimeField(_("posted on"), auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    class Meta:
        ordering = ["-timestamp"]

    # if self.image:
    #  imagefile = BytesIO()
    #         WIDTH_RES = 640
    #         htw = image.height / image.width
    #         #  im.convert('RGB')
    #         image = image.resize((WIDTH_RES, int(htw * WIDTH_RES)), Image.ANTIALIAS)
    #         image.save(imagefile, **save_kwargs)
    #         return imagefile
    # scaled_image = get_scaled_image()
    # if getattr(self, '_image_changed', True):
    #     small=rescale_image(self.image,width=100,height=100)
    #     self.image_small=SimpleUploadedFile(name,small_pic)

    def __str__(self):
        return gettext(f"{self.user.name} added a post on {self.timestamp}")


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=180)
    timestamp = models.DateTimeField(_("posted on"), auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return gettext(f"{self.user.name} commented on a post of {self.post.user.name}")
