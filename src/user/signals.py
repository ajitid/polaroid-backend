from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_init, post_save

from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    Profile.objects.create(user=instance)


@receiver(post_init, sender=Profile)
def init_previous_photo(sender, instance, **kwargs):
    instance.__previous_photo = instance.photo
    instance.__should_delete_previous_photo = False


@receiver(pre_save, sender=Profile)
def compare_with_previous_photo(sender, instance, **kwargs):
    # TODO use update_fields ^from here instead
    if (
        not instance.__previous_photo
        or instance.__previous_photo.name == sender.photo.field.default
        or instance.photo == instance.__previous_photo
    ):
        return
    instance.__should_delete_previous_photo = True


@receiver(post_save, sender=Profile)
def set_previous_photo(sender, instance, **kwargs):
    if instance.__should_delete_previous_photo:
        instance.__previous_photo.delete(False)
        instance.__should_delete_previous_photo = False
    instance.__previous_photo = instance.photo


@receiver(post_delete, sender=Profile)
def delete_profile_photo(sender, instance, **kwargs):
    if instance.photo.name == sender.photo.field.default:
        return
    instance.photo.delete(False)
