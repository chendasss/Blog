"""作品集模型：技能、项目、经历时间线。"""
import markdown
from django.db import models

from core.utils import unique_slugify


class Skill(models.Model):
    name = models.CharField("技能名称", max_length=50)
    category = models.CharField("分类", max_length=50, blank=True, help_text="如：语言 / 框架 / 数据库 / 工具与部署")
    level = models.PositiveSmallIntegerField("熟练度(1-5)", default=3)
    description = models.CharField("说明", max_length=200, blank=True)
    order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "技能"
        verbose_name_plural = "技能"
        ordering = ["category", "order", "id"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField("项目名", max_length=120)
    slug = models.SlugField("别名", max_length=140, unique=True, allow_unicode=True, blank=True)
    summary = models.CharField("一句话简介", max_length=200)
    description = models.TextField("详细介绍（Markdown）", blank=True)
    tech_stack = models.CharField("技术栈", max_length=200, blank=True, help_text="逗号分隔，如：Python,Django,爬虫")
    cover = models.ImageField("封面图", upload_to="projects/", blank=True)
    url = models.URLField("项目地址", blank=True)
    github = models.URLField("GitHub", blank=True)
    order = models.PositiveIntegerField("排序", default=0)
    is_featured = models.BooleanField("置顶/精选", default=False)

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目"
        ordering = ["-is_featured", "order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    @property
    def description_html(self):
        if not self.description:
            return ""
        return markdown.markdown(self.description, extensions=["fenced_code", "codehilite", "tables"])

    def __str__(self):
        return self.title


class CareerTimeline(models.Model):
    TYPE_CHOICES = [
        ("work", "工作"),
        ("education", "教育"),
        ("milestone", "项目里程碑"),
    ]
    type = models.CharField("类型", max_length=20, choices=TYPE_CHOICES, default="work")
    org = models.CharField("机构/公司", max_length=120)
    role = models.CharField("角色/职位", max_length=120, blank=True)
    start_date = models.DateField("开始时间", null=True, blank=True)
    end_date = models.DateField("结束时间", null=True, blank=True, help_text="留空表示至今")
    description = models.TextField("描述", blank=True)
    order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "经历时间线"
        verbose_name_plural = "经历时间线"
        ordering = ["-start_date", "order"]

    def __str__(self):
        return f"{self.org} · {self.role or ''}"
