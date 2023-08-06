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
    profile_photo = models.FileField()
    name = models.CharField(max_length=100, validators=[username_validator], null=True)
    Website = models.URLField(max_length=100, null=True)
    Bio = models.CharField(max_length=150, null=True)
    Phone_number = models.CharField(max_length=18, null=True, validators=[phone_validate])
    email = models.EmailField(_("email address"), blank=True)
    Gander = models.CharField(choices=Gander_choices, max_length=1, null=True, blank=True)
    story = models.FileField()

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


class VarificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField()
    is_varification = models.BooleanField()
    date = models.DateTimeField()



class UserStory(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_story')
    image = models.ImageField(null=True, blank=True )
    video = models.FileField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True)
    see_user = models.IntegerField(null=True, blank=True)
    expiration_time = models.DateTimeField(db_index=True)



