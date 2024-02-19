from django.shortcuts import render

def home_view(request):
    return render(request, 'blog/index.html')

def blog_posts(request):
    return render(request, 'blog/blog-post.html')

def about(request):
    return render(request, 'blog/about.html')