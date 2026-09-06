"""核心视图：首页、关于、求职、在线简历、搜索。"""
import re

from django.db.models import Q
from django.shortcuts import render
from django.utils.safestring import mark_safe

from blog.models import Post
from portfolio.models import CareerTimeline, Project, Skill

from .models import Profile, SiteSetting


def _group_skills(skills):
    groups = {}
    for skill in skills:
        groups.setdefault(skill.category or "其他", []).append(skill)
    return groups


def home(request):
    profile = Profile.load()
    site = SiteSetting.load()
    skills = Skill.objects.all()[:4]
    projects = Project.objects.filter(is_featured=True)[:3]
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED)[:4]
    return render(
        request,
        "core/home.html",
        {"profile": profile, "site": site, "skills": skills, "projects": projects, "posts": posts},
    )


def about(request):
    profile = Profile.load()
    skill_groups = _group_skills(Skill.objects.all())
    timeline = CareerTimeline.objects.all()
    return render(
        request,
        "core/about.html",
        {"profile": profile, "skill_groups": skill_groups, "timeline": timeline},
    )


def career(request):
    site = SiteSetting.load()
    profile = Profile.load()
    posts = Post.objects.filter(
        status=Post.STATUS_PUBLISHED,
        category__slug=site.career_category_slug,
    )[:10]
    return render(request, "core/career.html", {"site": site, "profile": profile, "posts": posts})


def resume(request):
    profile = Profile.load()
    skill_groups = _group_skills(Skill.objects.all())
    timeline = CareerTimeline.objects.all()
    projects = Project.objects.filter(is_featured=True)[:3]
    return render(
        request,
        "core/resume.html",
        {"profile": profile, "skill_groups": skill_groups, "timeline": timeline, "projects": projects},
    )


def _highlight(text, q):
    if not q or not text:
        return text
    return re.sub(re.escape(q), lambda m: f"<mark>{m.group(0)}</mark>", text, flags=re.IGNORECASE)


def _snippet(text, q, length=120):
    if not text:
        return ""
    idx = text.lower().find(q.lower())
    if idx == -1:
        return text[:length]
    start = max(0, idx - 30)
    return "…" + text[start : idx + len(q) + length] + "…"


def search(request):
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        posts = (
            Post.objects.filter(status=Post.STATUS_PUBLISHED)
            .filter(
                Q(title__icontains=q)
                | Q(excerpt__icontains=q)
                | Q(content__icontains=q)
                | Q(tags__name__icontains=q)
            )
            .select_related("category")
            .distinct()
        )
        for post in posts:
            results.append(
                {
                    "post": post,
                    "title_html": mark_safe(_highlight(post.title, q)),
                    "snippet_html": mark_safe(_highlight(_snippet(post.excerpt or post.content, q), q)),
                }
            )
    return render(request, "core/search.html", {"q": q, "results": results})
