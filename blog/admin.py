from django.contrib import admin
from .models import Post, Email

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['author', 'status']
    raw_id_fields = ['author']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-publish']

admin.site.register(Email)