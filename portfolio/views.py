"""作品集视图：项目列表、项目详情。"""
from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    projects = Project.objects.all()
    tech = request.GET.get("tech")

    all_techs = sorted({t for p in Project.objects.all() for t in p.tech_list})
    if tech:
        projects = projects.filter(tech_stack__icontains=tech)

    context = {
        "projects": projects,
        "all_techs": all_techs,
        "active_tech": tech,
    }
    return render(request, "portfolio/project_list.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "portfolio/project_detail.html", {"project": project})
