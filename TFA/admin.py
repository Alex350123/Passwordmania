from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Music

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'user_name', 'is_staff', 'is_active', 'display_music')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('email', 'user_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('user_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Music Preferences'), {'fields': ('music',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    def display_music(self, obj):
        return ', '.join([music.title for music in obj.music.all()])
    display_music.short_description = 'Music'

admin.site.register(CustomUser, CustomUserAdmin)

class MusicAdmin(admin.ModelAdmin):
    list_display = ('spotify_id', 'title', 'artist','preview_url')
    search_fields = ('title', 'artist')
    ordering = ('title',)

admin.site.register(Music, MusicAdmin)
