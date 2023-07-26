from django.contrib import admin

from user.models import User, UserStory , SavedPost

# Register your models here.
admin.site.register(User)
admin.site.register(UserStory)
admin.site.register(SavedPost)
