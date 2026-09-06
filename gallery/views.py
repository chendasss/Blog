"""相册视图：相册与照片墙。"""
from django.shortcuts import get_object_or_404, render

from .models import Album, GalleryPhoto


def gallery(request):
    albums = Album.objects.all()
    album_slug = request.GET.get("album")

    active_album = None
    photos = GalleryPhoto.objects.filter(is_public=True).select_related("album")
    if album_slug:
        active_album = get_object_or_404(Album, slug=album_slug)
        photos = photos.filter(album=active_album)

    context = {
        "albums": albums,
        "photos": photos,
        "active_album": active_album,
    }
    return render(request, "gallery/gallery.html", context)
