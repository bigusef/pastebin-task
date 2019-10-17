from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    the BaseModel will be using by all models will mapped to PostgreSQL
    to add some features to all models like timestamp
    """
    created = models.DateTimeField(_("Created Date"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated Date"), auto_now=True)

    class Meta:
        abstract = True
