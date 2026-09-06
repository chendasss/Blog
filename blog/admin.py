from django.contrib import admin

from .models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "is_featured", "published_at", "views")
    list_filter = ("status", "is_featured", "category")
    search_fields = ("title", "content")
    filter_horizontal = ("tags",)
    readonly_fields = ("views",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "tags", "status", "is_featured", "cover")}),
        ("内容", {"fields": ("excerpt", "content")}),
        ("时间", {"fields": ("published_at",)}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "content_short", "is_approved", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("name", "content")
    actions = ["approve", "mark_spam"]

    @admin.display(description="内容")
    def content_short(self, obj):
        return obj.content[:40]

    @admin.action(description="通过所选评论")
    def approve(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="标记为垃圾评论")
    def mark_spam(self, request, queryset):
        queryset.update(is_approved=False)
