from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404

from .models import Post, Team


def get_posts(request):
    posts = Post.objects.all()

    if category := request.GET.get("category", None):
        sponsor, name = category.split("-")
        team = get_object_or_404(Team, sponsor=sponsor, name=name)
        posts = posts.filter(category=team)

    paginator = Paginator(posts, 10)
    page = int(request.GET.get("page", 1))

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    return posts
