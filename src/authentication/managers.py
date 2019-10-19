from django.db import models


class ProfileManager(models.Manager):
    """
    extend default manager for user profile model and add new methods on it
    """
    def active(self, *args, **kwargs):
        """
        additional method to return only active users profile
        :pramters accept args and kwargs
        :return QuerySet
        """
        return self.filter(user__is_active=True, *args, **kwargs)
