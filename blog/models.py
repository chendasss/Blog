"""博客模型：分类、标签、文章、评论。"""
import re

import markdown
from django.db import models
from django.utils import timezone

from core.utils import unique_slugify


class Category(models.Model):
    name = models.CharField("名称", max_length=50)
    slug = models.SlugField("别名", max_length=60, unique=True, allow_unicode=True, blank=True)
    description = models.CharField("描述", max_length=200, blank=True)
    order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("名称", max_length=50)
    slug = models.SlugField("别名", max_length=60, unique=True, allow_unicode=True, blank=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "草稿"),
        (STATUS_PUBLISHED, "已发布"),
    ]

    title = models.CharField("标题", max_length=200)
    slug = models.SlugField("别名", max_length=220, unique=True, allow_unicode=True, blank=True)
    excerpt = models.TextField("摘要", blank=True, help_text="留空则列表页自动截取正文")
    content = models.TextField("正文（Markdown）")
    content_html = models.TextField("渲染后 HTML", blank=True, editable=False)
    cover = models.ImageField("封面图", upload_to="posts/", blank=True)

    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    is_featured = models.BooleanField("精选", default=False)
    views = models.PositiveIntegerField("阅读量", default=0, editable=False)

    category = models.ForeignKey(
        Category, verbose_name="分类", on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True, related_name="posts")

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    published_at = models.DateTimeField("发布时间", null=True, blank=True)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        self.content_html = markdown.markdown(
            self.content,
            extensions=["fenced_code", "codehilite", "tables"],
        )
        if not self.excerpt:
            plain = re.sub(r"<[^>]+>", "", self.content_html)
            self.excerpt = " ".join(plain.split())[:160]
        if self.status == self.STATUS_PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name="文章", on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", verbose_name="父评论", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    name = models.CharField("昵称", max_length=50)
    email = models.EmailField("邮箱（不公开）", blank=True)
    content = models.TextField("内容")
    is_approved = models.BooleanField("审核通过", default=False)
    created_at = models.DateTimeField("时间", auto_now_add=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.name}: {self.content[:30]}"

    @property
    def approved_replies(self):
        return self.replies.filter(is_approved=True)
