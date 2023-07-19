from django.contrib import admin

from .models import Comment, Post, Team


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "post"]
