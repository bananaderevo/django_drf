from django.contrib import admin
from .models import Comments, Posts


@admin.register(Posts)
class AdminPosts(admin.ModelAdmin):
    list_display = ['text']


@admin.register(Comments)
class AdminComments(admin.ModelAdmin):
    list_display = ['comment']