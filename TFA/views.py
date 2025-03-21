
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Music, CustomUser
from .spotify_service import get_spotify_token, search_tracks
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import CustomUserSerializer, LoginSerializer
from django.http import JsonResponse
import requests
import random

def spotify_search_view(request):
    client_id = 'fa6160056b324d3dba6f28b488af0acf'
    client_secret = '85ef8936372d480a8c722a6eee8896b2'
    token = get_spotify_token(client_id, client_secret)

    # print(f"Spotify Token: {token}")

    if not token:
        return JsonResponse({'error': 'Unable to authenticate with Spotify'}, status=400)

    query = request.GET.get('query', '')
    search_results = search_tracks(query, token)

    # print(f"Spotify API Response: {search_results}")

    filtered_tracks = []
    node_server_url = "http://localhost:3000/preview"

    for track in search_results.get("tracks", {}).get("items", []):
        title = track["name"]
        preview_url = track.get("preview_url")


        if not preview_url:
            try:
                node_response = requests.get(f"{node_server_url}?title={title}")
                if node_response.status_code == 200:
                    preview_data = node_response.json()
                    preview_url = preview_data.get("previewUrl", None)
                    print(f" Node.js  previewUrl: {preview_url}")
            except requests.RequestException as e:
                print(f" failto to fetch previewUrl: {e}")


        if preview_url:
            filtered_tracks.append({
                'spotify_id': track["id"],
                'title': title,
                'artist': ', '.join(artist["name"] for artist in track["artists"]),
                'preview_url': preview_url
            })

    print(f"filtered playlist: {filtered_tracks}")
    return JsonResponse({'tracks': filtered_tracks}, safe=False)


def select_music_view(request):
    return render(request,"selectmusic2.html")


@api_view(['POST'])
@permission_classes([AllowAny])
def save_music(request):
    user_id = request.data.get('user_id')  # get userid for auth
    spotify_ids = request.data.get('spotify_ids', [])

    user = get_object_or_404(CustomUser, id=user_id)
    user.music_authenticated = True
    user.save()
    music_objects = []

    for spotify_data in spotify_ids:
        spotify_id = spotify_data.get('spotify_id')
        title = spotify_data.get('title', 'Unknown')
        artist = spotify_data.get('artist', 'Unknown')
        preview_url = spotify_data.get('preview_url', '')


        music, created = Music.objects.update_or_create(
            spotify_id=spotify_id,
            defaults={'title': title, 'artist': artist, 'preview_url': preview_url}
        )
        music_objects.append(music)


    user.music.add(*music_objects)

    return Response({'message': 'Music updated/added successfully'}, status=status.HTTP_200_OK)


class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'email': user.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register_view(request):
    return render(request, 'register.html')

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,'id':user.id,'music_auth': user.music_authenticated}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    return render(request, 'login.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def load_music_preview(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'error': 'provided with no ID'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(CustomUser, id=user_id)
    music_ids = list(user.music.values_list('id', flat=True))
    random_ids = random.sample(music_ids, min(5, len(music_ids)))  
    user_music = Music.objects.filter(id__in=random_ids)

    tracks_details = [{
        'title': music.title,
        'artist': music.artist,
        'preview_url': music.preview_url
    } for music in user_music if music.preview_url]

    if not tracks_details:
        return Response({'error': 'No available preview urls'}, status=status.HTTP_404_NOT_FOUND)

    return Response(tracks_details, status=status.HTTP_200_OK)

def authenticate_view(request):
    return render(request,'music_authentication.html')
def pass_view(request):
    return render(request,"pass.html")