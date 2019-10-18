from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta

from .managers import PastesManager
from helper.models import BaseModel
from helper.utilities import code_generator


class Pastes(BaseModel):
    # region Class attribute
    NEVER = 0
    HOUR = 1
    DAY = 2
    WEEK = 3
    MONTH = 4

    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2
    # endregion

    # region Class choices
    EXPIRATION_CHOICE = (
        (NEVER, _('Never')),
        (HOUR, _('an Hour')),
        (DAY, _('a Day')),
        (WEEK, _('a Week')),
        (MONTH, _('a Month')),
    )

    PRIVACY_CHOICE = (
        (PUBLIC, _('Public')),
        (SHARED, _('Shared')),
        (PRIVATE, _('Private')),
    )
    # endregion

    author = models.ForeignKey('authentication.Profile', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=45)
    contect = models.TextField()
    expiration = models.IntegerField(choices=EXPIRATION_CHOICE, default=NEVER)
    expire_date = models.DateTimeField(null=True, blank=True, editable=False)
    privacy = models.IntegerField(choices=PRIVACY_CHOICE, default=PUBLIC)
    allowed_user = models.ManyToManyField('authentication.Profile', related_name='shared', blank=True)
    shortcode = models.SlugField(max_length=15, unique=True, blank=True, db_index=True)

    objects = PastesManager()

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwarg):
        if self.expiration == self.HOUR:
            self.expire_date = timezone.now() + relativedelta(hours=1)
        elif self.expiration == self.DAY:
            self.expire_date = timezone.now() + relativedelta(days=1)
        elif self.expiration == self.WEEK:
            self.expire_date = timezone.now() + relativedelta(weeks=1)
        elif self.expiration == self.MONTH:
            self.expire_date = timezone.now() + relativedelta(months=1)

        if not self.shortcode:
            self.shortcode = code_generator(self, 15)

        return super().save(*args, **kwarg)

    def get_absolute_url(self):
        return reverse('snippet:pastes-detail', kwargs={'shortcode': self.shortcode})

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expire_date if self.expire_date else False
