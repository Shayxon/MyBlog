from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home_view(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)    
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    
    return render(request, 'blog/index.html', {'posts':posts})

def blog_post(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year = year, publish__month = month, publish__day = day, slug = post)
    return render(request, 'blog/blog-post.html', {'post':post})

def about(request):
    return render(request, 'blog/about.html')