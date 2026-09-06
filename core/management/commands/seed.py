"""初始化站点基础数据：分类、个人资料、站点配置、示例技能/项目。

用法：python manage.py seed
"""
from django.core.management.base import BaseCommand

from blog.models import Category
from core.models import Profile, SiteSetting
from portfolio.models import Project, Skill


class Command(BaseCommand):
    help = "初始化站点基础数据（分类、个人资料、站点配置、示例技能/项目）"

    def handle(self, *args, **options):
        # 分类
        categories = [
            ("求职感悟", "career"),
            ("技术", "tech"),
            ("生活", "life"),
        ]
        for name, slug in categories:
            Category.objects.get_or_create(slug=slug, defaults={"name": name})
        self.stdout.write(self.style.SUCCESS("分类已就绪"))

        # 个人资料
        profile = Profile.load()
        if not profile.name:
            profile.name = "你的名字"
            profile.title = "Python 工程师 · 记录求职与生活"
            profile.bio = "这里写一段自我介绍，让访客快速了解你。"
            profile.save()
        self.stdout.write(self.style.SUCCESS("个人资料已就绪"))

        # 站点配置
        site = SiteSetting.load()
        if not site.site_name or site.site_name == "我的博客":
            site.site_name = "我的博客"
            site.site_description = "一个记录求职感悟、技能与生活的个人博客。"
            site.footer_text = "© 2026 · 用 Django 构建"
            site.save()
        self.stdout.write(self.style.SUCCESS("站点配置已就绪"))

        # 示例技能
        if not Skill.objects.exists():
            Skill.objects.bulk_create(
                [
                    Skill(name="Python", category="语言", level=5, description="主力开发语言"),
                    Skill(name="Django", category="框架", level=4, description="Web 后端开发"),
                    Skill(name="SQL", category="数据库", level=4, description="数据查询与建模"),
                    Skill(name="Linux / 部署", category="工具与部署", level=3, description="Nginx、Docker、CI"),
                ]
            )
        self.stdout.write(self.style.SUCCESS("示例技能已就绪"))

        # 示例项目
        if not Project.objects.exists():
            Project.objects.create(
                title="示例项目",
                summary="这是一个占位项目，请到后台修改为你的真实项目。",
                description="替换为项目详细介绍，可写 **Markdown**。",
                tech_stack="Python,Django",
                is_featured=True,
            )
        self.stdout.write(self.style.SUCCESS("示例项目已就绪"))

        self.stdout.write(self.style.SUCCESS("\n初始化完成，请到 /admin/ 后台完善内容。"))
