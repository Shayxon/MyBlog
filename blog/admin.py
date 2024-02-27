from django.contrib import admin
from .models import Post, Email, Comment

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['author', 'status']
    raw_id_fields = ['author']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-publish']

@admin.register(Comment)
class AdminPost(admin.ModelAdmin):
    list_display = ['post', 'name', 'email', 'comment']
    list_filter = ['post']
    raw_id_fields = ['post']

admin.site.register(Email)