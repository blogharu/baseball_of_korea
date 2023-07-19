from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class PostSearchForm(forms.Form):
    duration = forms.ChoiceField(
        label="",
        choices=(
            (datetime(year=1, month=1, day=1), "Duration"),
            (timezone.now() - timedelta(days=1), "1 day"),
            (timezone.now() - timedelta(days=7), "1 week"),
            (timezone.now() - relativedelta(months=1), "1 month"),
            (timezone.now() - relativedelta(months=6), "6 month"),
            (timezone.now() - relativedelta(years=1), "1 year"),
        ),
    )
    search_area = forms.ChoiceField(
        label="",
        choices=(
            ("title", "Title"),
            ("username", "Username"),
        ),
    )
    search = forms.CharField(label="", max_length=100, required=False)

    def get_filtered_posts(self, posts):
        cd = self.cleaned_data
        posts = posts.filter(created__gt=cd["duration"])
        if cd["search"]:
            match cd["search_area"]:
                case "username":
                    posts = posts.filter(user__username=cd["search"])
                case "title":
                    posts = posts.filter(title__icontains=cd["search"])
        return posts
