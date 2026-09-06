"""核心模型：个人资料与站点配置（均为单例）。"""
from django.db import models


class SingletonMixin:
    """单例模型辅助：通过 ``load()`` 取唯一一行。"""

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Profile(SingletonMixin, models.Model):
    name = models.CharField("姓名", max_length=100)
    title = models.CharField("一句话定位", max_length=200, blank=True)
    avatar = models.ImageField("头像", upload_to="profile/", blank=True)
    bio = models.TextField("自我介绍", blank=True)
    location = models.CharField("所在地", max_length=100, blank=True)
    email = models.EmailField("邮箱", blank=True)
    phone = models.CharField("电话", max_length=50, blank=True)
    github = models.URLField("GitHub", blank=True)
    blog_url = models.URLField("博客链接", blank=True)

    class Meta:
        verbose_name = "个人资料"
        verbose_name_plural = "个人资料"

    def __str__(self):
        return self.name or "个人资料"


class SiteSetting(SingletonMixin, models.Model):
    site_name = models.CharField("站点名", max_length=100, default="我的博客")
    site_description = models.CharField("站点描述", max_length=200, blank=True)
    footer_text = models.CharField("页脚文案", max_length=200, blank=True)

    # 求职相关
    job_seeking = models.BooleanField("求职中", default=False)
    job_status_text = models.CharField("求职状态文案", max_length=100, blank=True)
    job_target = models.CharField("目标方向", max_length=200, blank=True)
    job_available = models.BooleanField("可到岗", default=False)
    resume_file = models.FileField("简历 PDF", upload_to="resume/", blank=True)
    career_category_slug = models.CharField("求职感悟分类 slug", max_length=100, default="career")

    class Meta:
        verbose_name = "站点配置"
        verbose_name_plural = "站点配置"

    def __str__(self):
        return self.site_name
