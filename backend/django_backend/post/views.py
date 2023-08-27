from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Comment, Post, Team
from .templatetags.utils import get_query_parameters
from .utils import get_posts


def index(request):
    return render(request, "post/index.html", {})


def _logout(request):
    logout(request)
    return redirect(request.GET.get("next", "/"))


def post_list(request):
    return render(
        request,
        "post/post_list.html",
        {
            "posts": get_posts(request),
        },
    )


def post_detail(request, post_id):
    posts = get_posts(request)
    post = get_object_or_404(Post, id=post_id)
    comments = []
    for comment in post.comments.all():
        comments.append(comment)
        for child in comment.childs.all():
            comments.append(child)
    return render(
        request,
        "post/post_detail.html",
        {
            "posts": posts,
            "post": post,
            "comments": comments,
        },
    )

@login_required()
def post_create(request):
    category = request.GET.get("category", "None-None")
    sponsor, name = category.split("-")
    team = get_object_or_404(Team, sponsor=sponsor, name=name)
    if request.POST:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = Post(
                title=post_form.cleaned_data["title"],
                content=post_form.cleaned_data["content"],
                user=request.user,
                category=team,
            )
            post.save()
            return redirect(post.get_absolute_url(request))
    else:
        post_form = PostForm()
    return render(request, "post/post_create.html", {"post_form": post_form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.POST:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post.title = post_form.cleaned_data["title"]
            post.content = post_form.cleaned_data["content"]
            post.save()
            return redirect(post.get_absolute_url(request))
    else:
        post_form = PostForm(instance=post)
    return render(request, "post/post_edit.html", {"post_form": post_form})


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    query_parameters = get_query_parameters(request)
    return redirect(
        reverse("post:post_list") + f"?{query_parameters}"
        if query_parameters
        else reverse("post:post_list")
    )


def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if parent := request.POST.get("parent_id", None):
        parent = get_object_or_404(Comment, id=int(parent))
        if parent.parent is not None:
            raise ValueError("parent comment cannot have parent")
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = Comment(
            post=post,
            user=request.user,
            content=comment_form.cleaned_data["content"],
        )
        if parent:
            comment.parent = parent
        comment.save()
    return redirect(post.get_absolute_url(request))


def comment_delete(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(
        Comment, id=comment_id, user=request.user, post=post
    )
    comment.delete()
    return redirect(post.get_absolute_url(request))
