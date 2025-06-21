from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from .models import BlogPost, Category, Comment
from .serializers import BlogPostSerializer, BlogPostListSerializer, CategorySerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly

class BlogPostListCreateView(generics.ListCreateAPIView):
    """
    List all published blog posts or create a new post (authors only)
    """
    queryset = BlogPost.objects.filter(status='published')
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogPostListSerializer
        return BlogPostSerializer
    
    def get_queryset(self):
        queryset = BlogPost.objects.all()
        if not self.request.user.is_authenticated or not self.request.user.is_author:
            queryset = queryset.filter(status='published')
        return queryset
    
    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if post.status == 'published':
            post.published_at = timezone.now()
            post.save()
            
            # Send real-time notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'blog_updates',
                {
                    'type': 'post_created',
                    'message': {
                        'id': post.id,
                        'title': post.title,
                        'author': post.author.username,
                        'created_at': post.created_at.isoformat()
                    }
                }
            )

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a blog post
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        post = serializer.save()
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
            post.save()

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class CommentListCreateView(generics.ListCreateAPIView):
    """
    List comments for a post or create a new comment
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, is_approved=True, parent=None)
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        comment = serializer.save(author=self.request.user, post_id=post_id)
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'post_{post_id}',
            {
                'type': 'comment_added',
                'message': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.isoformat()
                }
            }
        )

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_posts(request):
    """
    Get current user's posts
    """
    posts = BlogPost.objects.filter(author=request.user)
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_drafts(request):
    """
    Get current user's draft posts
    """
    drafts = BlogPost.objects.filter(author=request.user, status='draft')
    serializer = BlogPostListSerializer(drafts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def publish_post(request, post_id):
    """
    Publish a draft post
    """
    try:
        post = BlogPost.objects.get(id=post_id, author=request.user)
        if post.status == 'draft':
            post.status = 'published'
            post.published_at = timezone.now()
            post.save()
            
            # Send real-time notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'blog_updates',
                {
                    'type': 'post_published',
                    'message': {
                        'id': post.id,
                        'title': post.title,
                        'author': post.author.username,
                        'published_at': post.published_at.isoformat()
                    }
                }
            )
            
            serializer = BlogPostSerializer(post)
            return Response(serializer.data)
        else:
            return Response({'error': 'Post is not a draft'}, status=status.HTTP_400_BAD_REQUEST)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def archive_post(request, post_id):
    """
    Archive a published post
    """
    try:
        post = BlogPost.objects.get(id=post_id, author=request.user)
        post.status = 'archived'
        post.save()
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def blog_stats(request):
    """
    Get blog statistics
    """
    total_posts = BlogPost.objects.filter(status='published').count()
    total_categories = Category.objects.count()
    total_comments = Comment.objects.filter(is_approved=True).count()
    
    # Additional stats
    recent_posts = BlogPost.objects.filter(status='published').order_by('-created_at')[:5]
    popular_posts = BlogPost.objects.filter(status='published').order_by('-views_count')[:5]
    
    return Response({
        'total_posts': total_posts,
        'total_categories': total_categories,
        'total_comments': total_comments,
        'recent_posts': BlogPostListSerializer(recent_posts, many=True).data,
        'popular_posts': BlogPostListSerializer(popular_posts, many=True).data
    })

@api_view(['GET'])
def search_posts(request):
    """
    Advanced search for blog posts
    """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')
    
    posts = BlogPost.objects.filter(status='published')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    if category:
        posts = posts.filter(category__slug=category)
    
    if tag:
        posts = posts.filter(tags__icontains=tag)
    
    posts = posts.order_by('-created_at')
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def posts_by_category(request, category_slug):
    """
    Get posts by category
    """
    try:
        category = Category.objects.get(slug=category_slug)
        posts = BlogPost.objects.filter(category=category, status='published').order_by('-created_at')
        serializer = BlogPostListSerializer(posts, many=True)
        return Response({
            'category': CategorySerializer(category).data,
            'posts': serializer.data
        })
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def posts_by_author(request, author_id):
    """
    Get posts by author
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        author = User.objects.get(id=author_id)
        posts = BlogPost.objects.filter(author=author, status='published').order_by('-created_at')
        serializer = BlogPostListSerializer(posts, many=True)
        return Response({
            'author': {
                'id': author.id,
                'username': author.username,
                'email': author.email,
                'bio': author.bio
            },
            'posts': serializer.data
        })
    except User.DoesNotExist:
        return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    """
    Like/Unlike a post (placeholder for future implementation)
    """
    try:
        post = BlogPost.objects.get(id=post_id, status='published')
        # This is a placeholder - you would implement a Like model
        return Response({'message': 'Post liked successfully'})
    except BlogPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def featured_posts(request):
    """
    Get featured posts (posts with featured_image)
    """
    posts = BlogPost.objects.filter(
        status='published', 
        featured_image__isnull=False
    ).exclude(featured_image='').order_by('-created_at')[:6]
    
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def trending_posts(request):
    """
    Get trending posts (most viewed in last 7 days)
    """
    from datetime import timedelta
    week_ago = timezone.now() - timedelta(days=7)
    
    posts = BlogPost.objects.filter(
        status='published',
        created_at__gte=week_ago
    ).order_by('-views_count')[:10]
    
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)
