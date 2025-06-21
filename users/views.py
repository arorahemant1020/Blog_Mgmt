from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserSerializer

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get or update user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    """List all users (public profiles)"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveAPIView):
    """Get user profile by ID"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get current user's statistics"""
    user = request.user
    if user.is_author:
        from blog.models import BlogPost, Comment
        post_count = BlogPost.objects.filter(author=user).count()
        published_count = BlogPost.objects.filter(author=user, status='published').count()
        draft_count = BlogPost.objects.filter(author=user, status='draft').count()
        total_views = sum(BlogPost.objects.filter(author=user).values_list('views_count', flat=True))
        total_comments = Comment.objects.filter(post__author=user, is_approved=True).count()
        
        return Response({
            'total_posts': post_count,
            'published_posts': published_count,
            'draft_posts': draft_count,
            'total_views': total_views,
            'total_comments': total_comments,
            'role': user.role
        })
    else:
        return Response({
            'role': user.role,
            'message': 'User is not an author'
        })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def authors_list(request):
    """Get list of all authors"""
    authors = User.objects.filter(role__in=['author', 'admin'], is_active=True)
    serializer = UserSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change user password"""
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(old_password):
        return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password changed successfully'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """Update user profile"""
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
