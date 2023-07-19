from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404

from .forms import PostSearchForm
from .models import Post, Team


def get_posts(request):
    posts = Post.objects.all().order_by("-created")

    if category := request.GET.get("category", None):
        sponsor, name = category.split("-")
        team = get_object_or_404(Team, sponsor=sponsor, name=name)
        posts = posts.filter(category=team)

    post_search_form = PostSearchForm(request.GET)
    if post_search_form.is_valid():
        posts = post_search_form.get_filtered_posts(posts=posts)

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
