from django.shortcuts import render
from .models import Post

def home_view(request):
    posts = Post.published.all()
    return render(request, 'blog/index.html', {'posts':posts})

def blog_posts(request):
    return render(request, 'blog/blog-post.html')

def about(request):
    return render(request, 'blog/about.html')