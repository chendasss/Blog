from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("<uslug:slug>/", views.project_detail, name="project_detail"),
]
