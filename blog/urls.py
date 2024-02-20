from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.blog_post, name='blog_post'),
    path('about/', views.about, name='about'),
    path('subscribe/', views.subscribe, name='subscribe')
]