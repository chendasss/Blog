"""相册模型：相册与照片。"""
from django.db import models

from core.utils import unique_slugify


class Album(models.Model):
    name = models.CharField("相册名", max_length=100)
    slug = models.SlugField("别名", max_length=120, unique=True, allow_unicode=True, blank=True)
    cover = models.ImageField("封面图", upload_to="albums/", blank=True)
    description = models.CharField("描述", max_length=200, blank=True)
    order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "相册"
        verbose_name_plural = "相册"
        ordering = ["order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryPhoto(models.Model):
    album = models.ForeignKey(Album, verbose_name="相册", on_delete=models.CASCADE, related_name="photos")
    title = models.CharField("标题", max_length=120, blank=True)
    image = models.ImageField("图片", upload_to="gallery/")
    description = models.TextField("描述", blank=True)
    taken_at = models.DateField("拍摄时间", null=True, blank=True)
    is_public = models.BooleanField("公开", default=True)
    order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        verbose_name = "照片"
        verbose_name_plural = "照片"
        ordering = ["order", "-taken_at", "id"]

    def __str__(self):
        return self.title or f"照片 {self.pk}"
