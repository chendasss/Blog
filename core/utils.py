"""通用工具函数。"""
from django.utils.crypto import get_random_string
from django.utils.text import slugify


def unique_slugify(instance, value, slug_field="slug"):
    """在同类对象内生成唯一 slug，冲突时追加短随机后缀。

    ``allow_unicode=True`` 使中文标题也能生成可读的 slug。
    """
    manager = instance.__class__._default_manager
    base = slugify(value, allow_unicode=True) or "item"
    slug = base
    while manager.exclude(pk=instance.pk).filter(**{slug_field: slug}).exists():
        slug = f"{base}-{get_random_string(4)}"
    return slug
