from django.contrib import admin
from .models import Post,reviewsData,reportPost,Comments
# Register your models here.

admin.site.register(Post)
admin.site.register(reviewsData)
admin.site.register(reportPost)
admin.site.register(Comments)