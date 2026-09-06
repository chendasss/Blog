from django.contrib import admin

from .models import Profile, SiteSetting


class SingletonAdmin(admin.ModelAdmin):
    """单例模型后台：只允许一条记录，禁止新增/删除，避免出现多条导致前端读到空记录。"""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Profile)
class ProfileAdmin(SingletonAdmin):
    fieldsets = (
        ("基本信息", {"fields": ("name", "title", "avatar", "bio", "location")}),
        ("联系方式", {"fields": ("email", "phone", "github", "blog_url")}),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(SingletonAdmin):
    fieldsets = (
        ("站点", {"fields": ("site_name", "site_description", "footer_text")}),
        (
            "求职",
            {
                "fields": (
                    "job_seeking",
                    "job_status_text",
                    "job_target",
                    "job_available",
                    "resume_file",
                    "career_category_slug",
                )
            },
        ),
    )
