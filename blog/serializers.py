from rest_framework import serializers
from .models import BlogPost, Category, Comment
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at']
        read_only_fields = ['slug']
    
    def get_posts_count(self, obj):
        return obj.blogpost_set.filter(status='published').count()

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'parent', 'replies', 'replies_count', 'created_at', 'updated_at']
        read_only_fields = ['author']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
    
    def get_replies_count(self, obj):
        return obj.replies.count()

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    comments_count = serializers.SerializerMethodField()
    tag_list = serializers.ReadOnlyField()
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author', 'category', 
            'category_id', 'status', 'featured_image', 'tags', 'tag_list',
            'views_count', 'comments_count', 'reading_time', 'created_at', 
            'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'author', 'views_count']
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    
    def get_reading_time(self, obj):
        # Estimate reading time (average 200 words per minute)
        word_count = len(obj.content.split())
        reading_time = max(1, round(word_count / 200))
        return f"{reading_time} min read"

class BlogPostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'category',
            'status', 'featured_image', 'tag_list', 'views_count',
            'comments_count', 'reading_time', 'created_at', 'published_at'
        ]
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    
    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        reading_time = max(1, round(word_count / 200))
        return f"{reading_time} min read"

class BlogPostCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating posts"""
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'excerpt', 'category', 'status', 'featured_image', 'tags']
