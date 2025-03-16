# serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Music, CustomUser

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['spotify_id', ]

    def create(self, validated_data):
        # 根据提供的 Spotify ID 创建或更新数据库中的记录
        return Music.objects.get_or_create(spotify_id=validated_data['spotify_id'])[0]

class CustomUserSerializer(serializers.ModelSerializer):
    music = MusicSerializer(many=True, read_only=True)  # 多对多关系，只读
    password = serializers.CharField(write_only=True)  # 密码字段不应返回给客户端

    class Meta:
        model = CustomUser
        fields = ['email', 'user_name', 'password', 'music']
        extra_kwargs = {'password': {'write_only': True}}  # 确保密码不会被读取

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            user_name=validated_data['user_name']
        )
        user.set_password(validated_data['password'])  # 使用 Django 的密码散列方法
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
