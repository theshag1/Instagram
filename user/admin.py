from django.contrib import admin

from user.models import User, UserStory

# Register your models here.
admin.site.register(User)
admin.site.register(UserStory)

