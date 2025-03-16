
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

def spotify_search_view(request):
    client_id = 'fa6160056b324d3dba6f28b488af0acf'
    client_secret = '85ef8936372d480a8c722a6eee8896b2'
    token = get_spotify_token(client_id, client_secret)

    if not token:
        return JsonResponse({'error': 'Unable to authenticate with Spotify'}, status=400)

    query = request.GET.get('query', '')
    search_results = search_tracks(query, token)  # 获取搜索结果
    filtered_tracks = []

    node_server_url = "http://localhost:3000/preview"  # Node.js 服务器地址

    for track in search_results.get("tracks", {}).get("items", []):
        preview_url = track.get("preview_url")  # 尝试获取 Spotify 提供的 preview_url

        if not preview_url:  # 如果没有预览 URL，尝试从 Node.js 获取
            try:
                response = requests.get(f"{node_server_url}?title={track['name']}")
                if response.status_code == 200:
                    preview_data = response.json()
                    preview_url = preview_data.get("previewUrl", None)
                    print(f"Fetched from Node.js: {preview_url}")  # 调试日志
            except requests.RequestException as e:
                print(f"Error fetching preview URL from Node.js: {e}")

        # 只返回有 preview_url 的歌曲
        if preview_url:
            filtered_tracks.append({
                'spotify_id': track["id"],
                'title': track["name"],
                'artist': ', '.join(artist["name"] for artist in track["artists"]),
                'preview_url': preview_url  # 确保返回的歌曲都带 `preview_url`
            })

    return JsonResponse({'tracks': filtered_tracks}, safe=False)

def select_music_view(request):
    return render(request,"selectmusic.html")

@api_view(['POST'])
@permission_classes([AllowAny])  # 如果注册时即调用此API，可能需要AllowAny
def save_music(request):
    user_id = request.data.get('user_id')  # 获取用户ID
    spotify_ids = request.data.get('spotify_ids', [])
    music_objects = []

    # 根据提供的用户ID获取用户对象
    user = get_object_or_404(CustomUser, id=user_id)

    for spotify_data in spotify_ids:
        spotify_id = spotify_data.get('spotify_id')
        # 查找现有的 Music 对象或创建新的（如果不存在）
        music, created = Music.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={'title': spotify_data.get('title', 'Unknown'), 'artist': spotify_data.get('artist', 'Unknown')}
        )
        music_objects.append(music)

    # 更新指定用户的 music 列表
    user.music.add(*music_objects)  # 使用 add 而不是 set 来避免移除现有关联
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
            user = serializer.validated_data  # 确保这里返回的是用户对象
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    return render(request, 'login.html')

def get_spotify_track_details(spotify_id, token):
    """从Spotify获取曲目详情，包括预览URL。"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://api.spotify.com/v1/tracks/{spotify_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 允许未登录用户查询（如果安全性允许）
def load_music_preview(request):
    """根据 user_id 从用户音乐库中随机加载歌曲预览"""

    user_id = request.query_params.get('user_id')  # 从请求参数获取 user_id
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)  # 获取特定用户
    else:
        if not request.user.is_authenticated:
            return Response({'error': '用户未认证，请提供 user_id 或登录'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user  # 默认使用当前登录用户

    user_music = user.music.all().order_by('?')[:5]  # 随机选择 5 首歌曲

    client_id = 'fa6160056b324d3dba6f28b488af0acf'
    client_secret = '85ef8936372d480a8c722a6eee8896b2'
    token = get_spotify_token(client_id, client_secret)

    tracks_details = []
    for music in user_music:
        track_details = get_spotify_track_details(music.spotify_id, token)
        if track_details and 'preview_url' in track_details:
            tracks_details.append({
                'title': track_details['name'],
                'artist': ', '.join(artist['name'] for artist in track_details['artists']),
                'preview_url': track_details['preview_url']
            })
        print(track_details)  # 调试信息

    return Response(tracks_details, status=status.HTTP_200_OK)

def authenticate_view(request):
    return render(request,'music_authentication.html')