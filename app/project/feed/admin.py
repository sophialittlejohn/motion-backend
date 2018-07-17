from django.contrib import admin
from project.feed.models import Like, Post, Profile, Friendship

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Profile)
admin.site.register(Friendship)
