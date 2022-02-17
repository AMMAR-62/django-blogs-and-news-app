from django.contrib import admin
from .models import Post, BlogModel, Profile
# Register your models here.
admin.site.register(Post)
admin.site.register(BlogModel)
admin.site.register(Profile)