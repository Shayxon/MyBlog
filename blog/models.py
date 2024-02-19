from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse

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
