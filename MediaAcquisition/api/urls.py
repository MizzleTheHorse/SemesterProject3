from django.urls import path
from .views import *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('add_youtube/<link>', add_youtube_audio, name='add_yt'),
    path('delete_track/<link>', delete_audio, name='delete_track'),
    path('get_track/<link>', get_audio, name='get_track'),
    path('get_all_tracks/', get_all_tracks, name='get_all_tracks'),
    path('add_custom/', add_custom_audio, name='add_custom'),
    path('get_metadata/<link>', get_metadata, name='get_metadata'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]