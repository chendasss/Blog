from django.contrib import admin

from .models import Album, GalleryPhoto


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 0
    fields = ("image", "title", "description", "taken_at", "is_public", "order")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    search_fields = ("name",)
    inlines = [GalleryPhotoInline]


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "album", "taken_at", "is_public", "order")
    list_filter = ("album", "is_public")
    search_fields = ("title", "description")
