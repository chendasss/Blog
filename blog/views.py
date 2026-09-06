"""博客视图：文章列表、文章详情、评论提交。"""
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Category, Comment, Post, Tag


def post_list(request):
    posts = (
        Post.objects.filter(status=Post.STATUS_PUBLISHED)
        .select_related("category")
        .prefetch_related("tags")
    )
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    active_category = None
    active_tag = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    paginator = Paginator(posts, getattr(settings, "POSTS_PER_PAGE", 8))
    page_obj = paginator.get_page(request.GET.get("page"))

    query_string = request.GET.copy()
    query_string.pop("page", None)

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "active_category": active_category,
        "active_tag": active_tag,
        "query_string": query_string.urlencode(),
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("category").prefetch_related("tags"),
        slug=slug,
        status=Post.STATUS_PUBLISHED,
    )

    # 简单阅读量统计：同一会话内去重
    session_key = f"post_viewed_{post.pk}"
    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
        request.session[session_key] = True
        post.refresh_from_db(fields=["views"])

    comments = post.comments.filter(is_approved=True, parent__isnull=True)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid() and not form.cleaned_data.get("honeypot"):
            comment = form.save(commit=False)
            comment.post = post
            parent_id = form.cleaned_data.get("parent_id")
            if parent_id:
                parent = Comment.objects.filter(pk=parent_id, post=post, is_approved=True).first()
                comment.parent = parent
            # 含链接的评论进入待审核，其余直接通过（后台仍可随时审核/删除）
            raw = comment.content
            comment.is_approved = not any(k in raw for k in ("http://", "https://", "www."))
            comment.save()
            messages.success(request, "评论已提交，感谢你的分享。" if comment.is_approved else "评论已提交，审核通过后显示。")
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = CommentForm()

    prev_post = (
        Post.objects.filter(status=Post.STATUS_PUBLISHED, published_at__lt=post.published_at)
        .order_by("-published_at")
        .first()
    )
    next_post = (
        Post.objects.filter(status=Post.STATUS_PUBLISHED, published_at__gt=post.published_at)
        .order_by("published_at")
        .first()
    )

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "prev_post": prev_post,
        "next_post": next_post,
    }
    return render(request, "blog/post_detail.html", context)
