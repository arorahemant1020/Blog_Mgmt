from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_documentation(request):
    """
    Complete API documentation for the Django Blog Backend
    """
    docs = {
        "title": "Django Blog Backend API",
        "description": "Complete REST API for a blogging platform with user management and real-time features",
        "base_url": f"{request.scheme}://{request.get_host()}/api/",
        "endpoints": {
            "Authentication": {
                "POST /auth/users/": "Register new user",
                "POST /auth/jwt/create/": "Login (get JWT tokens)",
            },
            "Users": {
                "GET /users/": "List all users",
                "GET /users/{id}/": "Get user by ID",
                "GET /users/profile/": "Get current user profile",
                "GET /users/authors/": "List all authors",
            },
            "Blog Posts": {
                "POST /blog/posts/": "Create new post (authors only)",
                "GET /blog/posts/{slug}/": "Get post by slug",
                "PUT /blog/posts/{slug}/": "Update post (author/admin only)",
                "DELETE /blog/posts/{slug}/": "Delete post (author/admin only)",
                "GET /blog/my-posts/": "Get current user's posts",
            },
        },
        "authentication": {
            "type": "JWT Bearer Token",
            "header": "Authorization: Bearer <token>",
            "note": "Get token from /auth/jwt/create/ endpoint"
        },
        "permissions": {
            "Public": "No authentication required",
            "Authenticated": "Valid JWT token required",
            "Author": "User must have 'author' or 'admin' role",
            "Owner": "User must be the owner of the resource",
        },
        "websocket_endpoints": {
            "ws://localhost:8000/ws/blog/": "General blog updates",
            "ws://localhost:8000/ws/blog/post/{id}/": "Post-specific updates (comments, etc.)",
        },
        "example_requests": {
            "Create Post": {
                "method": "POST",
                "url": "/api/blog/posts/",
                "headers": {"Authorization": "Bearer <token>"},
                "body": {
                    "title": "My Blog Post",
                    "content": "This is the content...",
                    "excerpt": "Short description",
                    "category_id": 1,
                    "status": "published",
                    "tags": "python, django, api"
                }
            },
            "Register User": {
                "method": "POST", 
                "url": "/api/auth/users/",
                "body": {
                    "username": "newuser",
                    "email": "user@example.com",
                    "password": "securepassword",
                    "role": "author"
                }
            }
        }
    }
    
    return Response(docs)
