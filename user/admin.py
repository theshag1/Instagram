from django.contrib import admin

from user.models import User, UserStory
from UserSavedData.models import SavedPost

# Register your models here.
admin.site.register(User)
admin.site.register(SavedPost)
admin.site.register(UserStory)
