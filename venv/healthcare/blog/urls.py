from django.urls import path
from .views import create_blog_post, list_blog_posts, list_blog_posts_by_category

urlpatterns = [
    path('create/', create_blog_post, name='create_blog_post'),
    path('', list_blog_posts, name='list_blog_posts'),
    path('<str:category>/', list_blog_posts_by_category, name='list_blog_posts_by_category'),
]
