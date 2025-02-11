from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload_video, name="upload_video"),
    path("stream", views.stream, name="stream")
]