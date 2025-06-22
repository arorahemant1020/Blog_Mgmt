from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostListSerializer
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly

class BlogPostListCreateView(generics.ListCreateAPIView):
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
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        post = serializer.save()
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
            post.save()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_posts(request):
    posts = BlogPost.objects.filter(author=request.user)
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def publish_post(request, post_id):
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

@api_view(['GET'])
def posts_by_author(request, author_id):
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

