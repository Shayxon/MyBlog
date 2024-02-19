from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('blog-posts/', views.blog_posts, name='blog_posts'),
    path('about/', views.about, name='about'),
]