from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Email, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from .forms import EmailForm, CommentForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

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
    form = CommentForm()
    comments = Comment.objects.filter(post = post)
    return render(request, 'blog/blog-post.html', {'post':post, 'form':form, 'comments':comments})

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
        if email not in emails and email != settings.EMAIL_HOST_USER:
            form.save()
            send_mail('👋 Welcome to Shayxon\'s Blog!',
                        "Hey there! "
                        "Thanks for joining My Blog! I'm pumped to have you with us. Here, we're all about making coding fun and easy to understand. "
                        "Whether you're just starting out or a seasoned pro, you'll find helpful tips, cool projects, and plenty of support from our community. "
                        "Feel free to dive into our posts, ask questions, and share your own coding adventures. Let's learn and grow together! "
                        "Happy coding! "
                        "Founder, Shayxon Toirjonov"
                      , 'settings.EMAIL_HOST_USER', [email], fail_silently=True)
            messages.success(request, "You subscribed succesfully!")
        else:
            messages.error(request, "Email already exists!")
    return redirect('home')

@require_POST
def comment(request, post_id):
    form = CommentForm(request.POST)
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if form.is_valid():
        if post:
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()

            return JsonResponse({'status':200})
    return JsonResponse({'status': 400})