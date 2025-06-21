#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Category

User = get_user_model()

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        print("Superuser created: admin@example.com / admin123")

def create_sample_categories():
    """Create sample categories"""
    categories = [
        {'name': 'Technology', 'description': 'Tech-related posts'},
        {'name': 'Lifestyle', 'description': 'Lifestyle and personal posts'},
        {'name': 'Business', 'description': 'Business and entrepreneurship'},
        {'name': 'Education', 'description': 'Educational content'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"Created category: {category.name}")

def main():
    print("Setting up database...")
    
    # Run migrations
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser and sample data
    create_superuser()
    create_sample_categories()
    
    print("Database setup complete!")

if __name__ == '__main__':
    main()
