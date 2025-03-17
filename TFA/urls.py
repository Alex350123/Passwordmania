from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import select_music_view,spotify_search_view,UserRegistrationAPIView, register_view, save_music, load_music_preview, authenticate_view,login_view,LoginAPIView, pass_view

urlpatterns = [
    path('select_music/', select_music_view, name='select-music'),
    path('spotify_search/', spotify_search_view, name='spotify-search'),
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-registration-api'),
    path('register/', register_view, name='register'),
    path('api/savemusic/', save_music, name='save_music-api'),
    path('api/loadmusic/', load_music_preview, name='load_music_preview-api'),
    path('authenticate/', authenticate_view, name='authenticate'),
    path('', login_view, name='login'),
    path('api/login/', LoginAPIView.as_view(), name='login-api'),
    path('pass/', pass_view, name='pass'),
]
