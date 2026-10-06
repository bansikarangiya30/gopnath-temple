from django.db import models

class MediaItem(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    caption = models.CharField(max_length=150, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_hero = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name

    @property
    def is_video(self):
        return self.file.name.lower().endswith(('.mp4', '.mov', '.webm', '.ogg', '.avi', '.mkv'))

    @property
    def is_image(self):
        return self.file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.jfif', '.webp'))


class Review(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'Guest'} — {self.rating}★"


class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    session_key = models.CharField(max_length=255, blank=True, db_index=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visited_at']
        verbose_name = 'Visitor Log'
        verbose_name_plural = 'Visitor Logs'

    def __str__(self):
        return f"Visitor from {self.ip_address or 'Unknown IP'} on {self.visited_at.strftime('%Y-%m-%d %H:%M')}"

