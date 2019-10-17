from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created = models.DateTimeField(_("Created Date"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated Date"), auto_now=True)

    class Meta:
        abstract = True
