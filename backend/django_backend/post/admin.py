from django.contrib import admin

from .models import Post, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["sponsor", "name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "category",
        "title",
        "content",
        "created",
        "updated",
    ]
