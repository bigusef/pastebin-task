from django.utils import timezone
from django.db import models


class PastesManager(models.Manager):
    def available(self, *args, **kwargs):
        return self.filter(
            models.Q(expire_date__gte=timezone.now()) | models.Q(expire_date__isnull=True),
            *args, **kwargs
        )

    def unavailable(self, *args, **kwargs):
        return self.filter(expire_date__lt=timezone.now(), *args, **kwargs)
