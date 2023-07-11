from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from items.validators import phone_validate
from items.choices import Gander_choices


# Create your models here.

class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    # un showed information
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=100, validators=[username_validator], null=True)
    Website = models.URLField(max_length=100, null=True)
    Bio = models.CharField(max_length=150, null=True)
    Phone_number = models.CharField(max_length=18, null=True, validators=[phone_validate])
    email = models.EmailField(_("email address"), blank=True)
    Gander = models.CharField(choices=Gander_choices, max_length=1, null=True, blank=True)

    # showed information

    @property
    def follower(self):
        return self.follow_user.count()

    @property
    def followed(self):
        return self.follower_user.count()

    @property
    def post(self):
        return self.post_user.count()