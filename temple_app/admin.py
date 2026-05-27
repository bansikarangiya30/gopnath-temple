from django.contrib import admin
from django.utils.html import format_html
from temple_app.models import MediaItem, Review

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_thumbnail', 'file', 'uploaded_at', 'is_video', 'is_hero')
    list_filter = ('uploaded_at', 'is_hero')
    search_fields = ('file',)
    readonly_fields = ('display_preview',)

    def display_thumbnail(self, obj):
        if obj.is_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.file.url)
        return "Video/File"
    display_thumbnail.short_description = 'Thumbnail'

    def display_preview(self, obj):
        if obj.is_image:
            return format_html('<img src="{}" style="max-width: 400px; max-height: 400px;" />', obj.file.url)
        return "No preview available for this file type."
    display_preview.short_description = 'Preview'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'email', 'comment')
