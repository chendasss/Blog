"""项目根 URL 配置。"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, register_converter
from django.urls.converters import StringConverter


class UnicodeSlugConverter(StringConverter):
    """支持中文等 Unicode 字符的 slug 转换器（默认 slug 只匹配 ASCII）。"""

    regex = r"[-\w]+"


register_converter(UnicodeSlugConverter, "uslug")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("blog/", include("blog.urls")),
    path("projects/", include("portfolio.urls")),
    path("gallery/", include("gallery.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
