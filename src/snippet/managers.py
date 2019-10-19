from django.utils import timezone
from django.db import models


class PastesManager(models.Manager):
    """
    override default manager to add new methods and function
    """
    def available(self, *args, **kwargs):
        """
        this method will return all avalible Pastes
        :return Pastes QuerySet
        """
        return self.filter(
            models.Q(expire_date__gte=timezone.now()) | models.Q(expire_date__isnull=True),
            *args, **kwargs
        )

    def unavailable(self, *args, **kwargs):
        """
        this method will return all expire Pastes
        :return Pastes QuerySet
        """
        return self.filter(expire_date__lt=timezone.now(), *args, **kwargs)
