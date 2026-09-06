from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("career/", views.career, name="career"),
    path("resume/", views.resume, name="resume"),
    path("search/", views.search, name="search"),
]
