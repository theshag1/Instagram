from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_validate(value):
    if not value.startswith(('+1', '+7', '+65', '+998')):
        raise ValidationError(_('Your phone is not required ! '))
