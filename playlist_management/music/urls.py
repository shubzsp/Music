from django.urls import path,include
from music.views import PlaylistApiView
from rest_framework import routers

playlist_router = routers.DefaultRouter()
playlist_router.register(r'playlist',PlaylistApiView)
urlpatterns = [
    path('',include(playlist_router.urls)),
]
