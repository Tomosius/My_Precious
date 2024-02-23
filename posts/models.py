# posts/models.py

import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy

# Constants for determining the uncertainty of the event date.
DATE_UNCERTAINTY_CHOICES = [
    ('0', 'exact'),
    ('1', '1 day'),
    ('3', '3 days'),
    ('7', 'week'),
    ('14', '2 weeks'),
    ('30', 'month'),
    ('90', '3 months'),
]


class Post(PolymorphicModel):
    """
    Base model for representing a post, with attributes shared by both
    LostPost and FoundPost subclasses. This model uses Django Polymorphic
    to allow for querying on the base model and automatically returning
    instances of the child models.

    Attributes: title (models.CharField): The title of the post. description
    (models.TextField): A detailed description of the item or pet lost/found.
    user (models.ForeignKey): Reference to the user who created the post.
    created_at (models.DateTimeField): The date and time the post was
    created. updated_at (models.DateTimeField): The date and time the post
    was last updated. latitude (models.DecimalField): Latitude for the
    location of the event (optional). longitude (models.DecimalField):
    Longitude for the location of the event (optional). slug (
    models.SlugField): A URL-friendly slug derived from the post title and
    ID. event_date (models.DateField): The date of the event (lost/found).
    date_uncertainty_days (models.CharField): Represents how certain the
    event date is.
    """

    class Meta:
        ordering = ['-created_at']  # Ensures posts are displayed newest first.

    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=64, decimal_places=44, null=True,
                                   blank=True)
    longitude = models.DecimalField(max_digits=64, decimal_places=44, null=True,
                                    blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    event_date = models.DateField(default=datetime.date.today)
    date_uncertainty_days = models.CharField(
        max_length=10,
        choices=DATE_UNCERTAINTY_CHOICES,
        default='0',
        help_text="Select how much the actual event date could differ."
    )

    def __str__(self):
        """Return the title of the post for display."""
        return self.title

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique slug. If the post is
        being created (not updated), it first saves to obtain an ID,
        then generates the slug and saves again. If the title is updated,
        the slug is regenerated.
        """
        prefix = 'f' if isinstance(self, FoundPost) else 'l'
        if not self.id or self._state.adding is True:
            # Initial save to get an ID for slug generation
            super().save(*args, **kwargs)
            self.slug = f"{slugify(self.title)}-{self.id}-{prefix}"
        else:
            # Check if the title has changed, and update slug if necessary
            original = type(self).objects.get(id=self.id)
            if original.title != self.title:
                self.slug = f"{slugify(self.title)}-{self.id}-{prefix}"
        super().save(*args, **kwargs)  # Final save with updated slug

    def get_dynamic_url(self):
        """
        Generates a URL based on the post type. This method checks the instance
        type and returns the appropriate URL for LostPost or FoundPost.

        Returns:
            str: The URL to the post's detail view.
        """
        if isinstance(self, LostPost):
            return reverse('lost_post_details', kwargs={'slug': self.slug})
        elif isinstance(self, FoundPost):
            return reverse('found_post_details', kwargs={'slug': self.slug})
        else:
            return "#"  # Fallback URL

    def post_type(self):
        """
        Identifies the type of the post instance.

        Returns: str: A string indicating whether the instance is a LostPost,
        FoundPost, or unknown type.
        """
        if isinstance(self, LostPost):
            return 'LostPost'
        elif isinstance(self, FoundPost):
            return 'FoundPost'
        return 'Unknown'


# Subclass definitions for LostPost and FoundPost, along with LostPhoto and
# FoundPhoto, follow the same structure and documentation principles as the
# Post class.

class LostPost(Post):
    def get_absolute_url(self):
        return reverse('posts:lost_post_details', kwargs={'slug': self.slug})


class FoundPost(Post):
    def get_absolute_url(self):
        return reverse('posts:found_post_details', kwargs={'slug': self.slug})


# Assuming LostPost and FoundPost classes are defined in the same file or
# imported appropriately

class LostPhoto(models.Model):
    """
    Represents a photo related to a LostPost.

    Attributes: image (CloudinaryField): An optional field for storing an
    image in Cloudinary. caption (models.CharField): An optional caption for
    the photo. lost_post (models.ForeignKey): A reference to the associated
    LostPost.
    """

    image = CloudinaryField('image', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    lost_post = models.ForeignKey('LostPost', related_name='photos',
                                  on_delete=models.CASCADE)

    def __str__(self):
        """Returns a descriptive string representation of the LostPhoto
        instance."""
        return f"Lost Photo for {self.lost_post.title}"

    def delete(self, *args, **kwargs):
        """
        Custom delete method to ensure the image is also deleted from Cloudinary
        before the LostPhoto object is deleted from the database.
        """
        if self.image:
            destroy(self.image.public_id)  # Deletes the image from Cloudinary
        super().delete(*args,
                       **kwargs)  # Proceeds with the default deletion process


class FoundPhoto(models.Model):
    """
    Represents a photo related to a FoundPost.

    Attributes: image (CloudinaryField): An optional field for storing an
    image in Cloudinary. caption (models.CharField): An optional caption for
    the photo. found_post (models.ForeignKey): A reference to the associated
    FoundPost.
    """

    image = CloudinaryField('image', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    found_post = models.ForeignKey('FoundPost', related_name='photos',
                                   on_delete=models.CASCADE)

    def __str__(self):
        """Returns a descriptive string representation of the FoundPhoto
        instance."""
        return f"Found Photo for {self.found_post.title}"

    def delete(self, *args, **kwargs):
        """
        Custom delete method to ensure the image is also deleted from Cloudinary
        before the FoundPhoto object is deleted from the database.
        """
        if self.image:
            destroy(self.image.public_id)  # Deletes the image from Cloudinary
        super().delete(*args,
                       **kwargs)  # Proceeds with the default deletion process
