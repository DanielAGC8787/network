from django.contrib import admin
from .models import Following, Post, User, Follower

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Following)
admin.site.register(Follower)

# Register your models here.
