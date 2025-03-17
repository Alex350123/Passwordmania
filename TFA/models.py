from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

class Music(models.Model):
    spotify_id = models.CharField(max_length=255, unique=True)  # Spotify 的唯一标识符
    title = models.CharField(max_length=255)  # 歌曲标题
    artist = models.CharField(max_length=255)  # 艺术家名字
    preview_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"  # 返回歌曲信息，便于管理和调试

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(_('user name'), max_length=150)  # 确保这个字段被定义
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    music = models.ManyToManyField(Music, blank=True)  # 确保这一行

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']  # 现在是正确的

    objects = CustomUserManager()

    def __str__(self):
        return self.email
