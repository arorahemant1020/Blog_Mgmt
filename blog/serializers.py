from rest_framework import serializers
from .models import BlogPost
from users.serializers import UserSerializer


class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tag_list = serializers.ReadOnlyField()
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author', 
            'status', 'featured_image', 'tags', 'tag_list',
            'views_count', 'reading_time', 'created_at', 
            'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'author', 'views_count']
    
    
    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        reading_time = max(1, round(word_count / 200))
        return f"{reading_time} min read"

class BlogPostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author',
            'status', 'featured_image', 'tag_list', 'views_count',
            'reading_time', 'created_at', 'published_at'
        ]
    
    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        reading_time = max(1, round(word_count / 200))
        return f"{reading_time} min read"

class BlogPostCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating posts"""
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'excerpt', 'status', 'featured_image', 'tags']
