from django.urls import path
from . import views

urlpatterns = [
    # Blog Posts
    path('posts/', views.BlogPostListCreateView.as_view(), name='post-list-create'),
    path('posts/<slug:slug>/', views.BlogPostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/publish/', views.publish_post, name='publish-post'),
    path('posts/<int:post_id>/archive/', views.archive_post, name='archive-post'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<slug:category_slug>/posts/', views.posts_by_category, name='posts-by-category'),
    
    # Comments
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
    # User-specific endpoints
    path('my-posts/', views.my_posts, name='my-posts'),
    path('my-drafts/', views.my_drafts, name='my-drafts'),
    path('authors/<int:author_id>/posts/', views.posts_by_author, name='posts-by-author'),
    
    # Search and filtering
    path('search/', views.search_posts, name='search-posts'),
    path('featured/', views.featured_posts, name='featured-posts'),
    path('trending/', views.trending_posts, name='trending-posts'),
    
    # Statistics
    path('stats/', views.blog_stats, name='blog-stats'),
]
