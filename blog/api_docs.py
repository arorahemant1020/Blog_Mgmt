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
                "PUT /users/profile/": "Update current user profile",
                "POST /users/profile/update/": "Update profile (alternative)",
                "POST /users/change-password/": "Change password",
                "GET /users/authors/": "List all authors",
            },
            "Blog Posts": {
                "GET /blog/posts/": "List published posts (with filtering)",
                "POST /blog/posts/": "Create new post (authors only)",
                "GET /blog/posts/{slug}/": "Get post by slug",
                "PUT /blog/posts/{slug}/": "Update post (author/admin only)",
                "DELETE /blog/posts/{slug}/": "Delete post (author/admin only)",
                "POST /blog/posts/{id}/publish/": "Publish draft post",
                "POST /blog/posts/{id}/archive/": "Archive post",
                "POST /blog/posts/{id}/like/": "Like/unlike post",
                "GET /blog/my-posts/": "Get current user's posts",
                "GET /blog/my-drafts/": "Get current user's drafts",
                "GET /blog/featured/": "Get featured posts",
                "GET /blog/trending/": "Get trending posts",
            },
            "Categories": {
                "GET /blog/categories/": "List all categories",
                "POST /blog/categories/": "Create category",
                "GET /blog/categories/{slug}/": "Get category by slug",
                "PUT /blog/categories/{slug}/": "Update category",
                "DELETE /blog/categories/{slug}/": "Delete category",
                "GET /blog/categories/{slug}/posts/": "Get posts by category",
            },
            "Comments": {
                "GET /blog/posts/{id}/comments/": "List post comments",
                "POST /blog/posts/{id}/comments/": "Add comment to post",
                "GET /blog/comments/{id}/": "Get comment by ID",
                "PUT /blog/comments/{id}/": "Update comment (owner only)",
                "DELETE /blog/comments/{id}/": "Delete comment (owner only)",
            },
            "Search & Discovery": {
                "GET /blog/search/?q={query}": "Search posts by title/content",
                "GET /blog/search/?category={slug}": "Filter by category",
                "GET /blog/search/?tag={tag}": "Filter by tag",
                "GET /blog/authors/{id}/posts/": "Get posts by author",
            },
            "Statistics": {
                "GET /blog/stats/": "Get blog statistics",
                "GET /users/stats/": "Get user statistics",
            }
        },
        "query_parameters": {
            "Posts Filtering": {
                "category": "Filter by category ID",
                "author": "Filter by author ID", 
                "status": "Filter by status (published/draft/archived)",
                "search": "Search in title/content",
                "ordering": "Order by (created_at, updated_at, views_count)",
                "page": "Page number for pagination",
            }
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
