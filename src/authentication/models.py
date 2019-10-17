from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from helper.models import BaseModel

from .managers import ProfileManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user realization based on Django AbstractUser and PermissionMixin.
    """

    # internal attribute
    __username_validator = UnicodeUsernameValidator()

    # DB Attribute
    username = models.CharField(
        _('username'),
        max_length=15,
        unique=True,
        help_text=_('Required. 15 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[__username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    # this is needed to use this model with django auth as a custom user class
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        managed = True
        abstract = False
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(BaseModel):
    MALE = 1
    FEMALE = 2

    GENDER_CHOICE = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICE, default=MALE)
    birth_date = models.DateField(null=True, blank=True)

    objects = ProfileManager()

    class Meta:
        managed = True
        abstract = False
        db_table = 'auth_user_profile'
        verbose_name = _('user profile')
        verbose_name_plural = _('users profile')

    @property
    def full_name(self) -> str:
        """
        if user have first_name and last_name
        Return the first_name plus the last_name, with a space in between.
        Or will return empty stringn
        """
        if self.first_name or self.last_name:
            space = ' ' if self.first_name else ''
            return ''.join([
                self.first_name,
                space,
                self.last_name
            ])
        else:
            return ''

    @property
    def age(self) -> int:
        """
        Return the user age based on birth date
        """
        if self.birth_date:
            today = timezone.now().date()
            days = (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            return today.year - self.birth_date.year - days
        else:
            return 0
