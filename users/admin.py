# admin.py for the 'users' Django app

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    """
    Defines the inline admin settings for UserProfile.

    This class makes it possible to edit UserProfile instances
    directly within the User model admin page. It is set up as a stacked
    inline which means that the fields of the UserProfile will be stacked
    vertically for a cleaner user interface.
    """
    model = UserProfile
    can_delete = False  # Prevents deletion of the inline item
    verbose_name_plural = 'profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    """
    Extends the default UserAdmin class to include a UserProfile inline.

    This customization enables the admin to edit user profiles when managing
    User instances. It adds the UserProfileInline to the User model's admin
    interface, allowing for direct manipulation of user profiles within the
    same admin page as user details.
    """
    inlines = (UserProfileInline, )

    def get_inline_instances(self, request, obj=None):
        """
        Customizes inline instances based on the request or object context.

        Ensures that the UserProfile inline is only added when a User object
        exists, preventing errors on the creation of a new User. This method
        is particularly useful for avoiding the display of the inline form
        when adding a new User instance, as the UserProfile does not yet exist.
        """
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Unregister the original User admin to replace it with the customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Optional: Register UserProfile to manage it independently from the User model
# If you need to manage UserProfile independently, uncomment the next line.
# admin.site.register(UserProfile)
