from django.db import models


class ProfileManager(models.Manager):

    def active(self, *args, **kwargs):
        return self.filter(user__is_active=True, *args, **kwargs)
