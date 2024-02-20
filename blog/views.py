from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Email
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from .forms import EmailForm
from django.contrib import messages

def home_view(request):
    email_form = EmailForm()
    post_list = Post.published.all()
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)    
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    
    return render(request, 'blog/index.html', {'posts':posts, 'email_form':email_form})

def blog_post(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year = year, publish__month = month, publish__day = day, slug = post)
    return render(request, 'blog/blog-post.html', {'post':post})

def about(request):
    email_form = EmailForm()
    return render(request, 'blog/about.html', {'email_form':email_form})

@require_POST
def subscribe(request):
    emails = Email.objects.all()
    emails = emails.values_list('email', flat=True)
    form = EmailForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        if email not in emails:
            form.save()
            messages.success(request, "You subscribed succesfully!")
        else:
            messages.error(request, "Email already exists!")
    return redirect('home')