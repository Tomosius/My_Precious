from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


# UserProfile model to store user profile information
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    user_photo = CloudinaryField('image', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# Model to store social media links for a user
class SocialMediaLink(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name='social_media_links')
    name = models.CharField(max_length=50)  # e.g., Facebook, Twitter, LinkedIn
    url = models.URLField()

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.name}"


# Model to store languages spoken by a user
class Language(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name='languages')
    language = models.CharField(max_length=50)  # e.g., English, Spanish

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.language}"


# Signal to create or update UserProfile whenever a User instance is saved
# noinspection PyUnusedLocal
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(instance, created, **kwargs):
    # **kwargs value is needed for creating profile
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # This should be instance.profile.save() only if the profile already
        # exists. Consider using get_or_create to handle this.
        instance.profile, created = UserProfile.objects.get_or_create(
            user=instance)
        if not created:
            instance.profile.save()
