## **API Endpoints**

- `POST /api/auth/users/` - User registration
- `POST /api/auth/jwt/create/` - Login (get JWT tokens)
- `GET /api/blog/posts/` - List published posts
- `POST /api/blog/posts/` - Create new post (authors only)
- `GET /api/blog/posts/{slug}/` - Get post details
- `PUT /api/blog/posts/{slug}/` - Update post (author/admin only)
- `DELETE /api/blog/posts/{slug}/` - Delete post (author/admin only)
- `GET /api/blog/categories/` - List categories
- `POST /api/blog/posts/{id}/comments/` - Add comment