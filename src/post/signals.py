from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from .models import Post


class CacheFileState(object):
    EXISTS = "exists"
    GENERATING = "generating"
    DOES_NOT_EXIST = "does_not_exist"


@receiver(post_delete, sender=Post)
def delete_post_photo(sender, instance, **kwargs):
    instance.thumbnail.storage.delete(instance.thumbnail)
    instance.thumbnail.cachefile_backend.set_state(instance.thumbnail, CacheFileState.DOES_NOT_EXIST)
    instance.photo.delete(save=False)
    # FIXME deleting thumbnail
    # https://github.com/matthewwithanm/django-imagekit/issues/229#issuecomment-385145019
    # deleting thumnail doesn't removes it's folder in which it is present
