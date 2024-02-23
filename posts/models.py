# posts/models.py
import datetime

from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel

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
    Represents a general post, either lost or found, with common attributes.

    Attributes:
        title (models.CharField): The title of the post.
        description (models.TextField): A detailed description of the post.
        user (models.ForeignKey): The user who created the post.
        ...
    """

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
        return self.title

    def save(self, *args, **kwargs):
        prefix = 'f' if isinstance(self, FoundPost) else 'l'
        if not self.id or self._state.adding is True:
            super().save(*args, **kwargs)  # Initial save to get an ID
            self.slug = f"{slugify(self.title)}-{self.id}-{prefix}"
        else:
            original = type(self).objects.get(id=self.id)
            if original.title != self.title:
                self.slug = f"{slugify(self.title)}-{self.id}-{prefix}"
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def get_dynamic_url(self):
        if isinstance(self, LostPost):
            return reverse('lost_post_details', kwargs={'slug': self.slug})
        elif isinstance(self, FoundPost):
            return reverse('found_post_details', kwargs={'slug': self.slug})
        else:
            return "#"  # Fallback URL, in case it's neither

    def post_type(self):
        if isinstance(self, LostPost):
            return 'LostPost'
        elif isinstance(self, FoundPost):
            return 'FoundPost'
        return 'Unknown'


class LostPost(Post):
    def get_absolute_url(self):
        return reverse('posts:lost_post_details', kwargs={'slug': self.slug})


class FoundPost(Post):
    def get_absolute_url(self):
        return reverse('posts:found_post_details', kwargs={'slug': self.slug})


class LostPhoto(models.Model):
    image = CloudinaryField('image', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    lost_post = models.ForeignKey(LostPost, related_name='photos',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"Lost Photo for {self.lost_post.title}"

    def delete(self, *args, **kwargs):
        if self.image:
            destroy(self.image.public_id)
        super().delete(*args, **kwargs)


class FoundPhoto(models.Model):
    image = CloudinaryField('image', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    found_post = models.ForeignKey(FoundPost, related_name='photos',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return f"Found Photo for {self.found_post.title}"

    def delete(self, *args, **kwargs):
        if self.image:
            destroy(self.image.public_id)
        super().delete(*args, **kwargs)
