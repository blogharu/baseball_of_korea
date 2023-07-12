from django.shortcuts import render

from .utils import get_posts


def index(request):
    return render(request, "post/index.html", {})


def post_list(request):
    return render(
        request,
        "post/post_list.html",
        {
            "posts": get_posts(request),
        },
    )
