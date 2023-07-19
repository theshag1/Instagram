import datetime

from django.db import models


# Create your models here.


class UpdateCode(models.Model):
    email = models.EmailField()
    code = models.CharField()
    is_check = models.BooleanField(default=False)
    data_sent = models.DateTimeField(default=datetime.datetime.now())
