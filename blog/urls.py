from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.BlogPostListCreateView.as_view(), name='post-list-create'),
    path('posts/<slug:slug>/', views.BlogPostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/publish/', views.publish_post, name='publish-post'),
    path('my-posts/', views.my_posts, name='my-posts'),
    
]
