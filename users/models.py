from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    # Using CloudinaryField for image uploads
    user_photo = CloudinaryField('image', blank=True,
                                 null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Signal to create or update UserProfile whenever a User instance is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(instance, created, **kwargs):
    if created:
        # Explicitly create a new UserProfile only if the User instance is new.
        UserProfile.objects.create(user=instance)
    else:
        # For existing users, just save the profile. This assumes a profile
        # already exists. You might want to ensure it exists or handle cases
        # where it might not.
        instance.profile.save()
