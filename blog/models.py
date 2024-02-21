from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse
from django.core.mail import send_mass_mail
from django.conf import settings

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset() \
                                    .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to='media/%Y/%m/%d/', blank=False)
    body = CKEditor5Field(blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self) -> str:
        return self.title    

    def get_absolute_url(self):
        return reverse('blog_post', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
    def save(self, *args, **kwargs):
        if self.pk and self.status == self.Status.PUBLISHED:
            emails = Email.objects.all()
            emails = emails.values_list('email', flat=True)
            messages = [
                (
                f"New Post: {self.title}",
                f"You can read the post here: localhost:8000{self.get_absolute_url()}",
                'settings.EMAIL_HOST_USER',
                emails
                )
            ]

            send_mass_mail(messages, fail_silently=True)
        return super().save(*args, **kwargs)

class Email(models.Model):
    email = models.EmailField()
    subscribed = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.email