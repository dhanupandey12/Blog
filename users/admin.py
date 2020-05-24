from django.contrib import admin
from .models import Profile,MessageData,Notifications,Following,Followers
# Register your models here.

admin.site.register(Profile)
admin.site.register(MessageData)
admin.site.register(Notifications)
admin.site.register(Following)
admin.site.register(Followers)