from django.contrib import admin

from .models import CareerTimeline, Project, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "order")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tech_stack", "is_featured", "order")
    list_filter = ("is_featured",)
    search_fields = ("title", "summary", "description", "tech_stack")
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "description", "tech_stack", "cover")}),
        ("链接与排序", {"fields": ("url", "github", "order", "is_featured")}),
    )


@admin.register(CareerTimeline)
class CareerTimelineAdmin(admin.ModelAdmin):
    list_display = ("org", "role", "type", "start_date", "end_date", "order")
    list_filter = ("type",)
    search_fields = ("org", "role", "description")
