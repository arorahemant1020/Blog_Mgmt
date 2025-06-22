# Django Blog Backend API

A complete REST API for a blogging platform built with Django, featuring user management, JWT authentication, real-time updates with WebSockets, and comprehensive blog functionality.

## 🚀 Features

- **User Management**: Registration, authentication, and role-based permissions
- **Blog Posts**: Create, read, update, delete blog posts with rich content
- **Real-time Updates**: WebSocket support for live notifications
- **JWT Authentication**: Secure token-based authentication
- **Role-based Permissions**: Admin, Author, and Reader roles
- **RESTful API**: Clean, well-documented REST endpoints

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Real-time**: Django Channels with Redis
- **API Documentation**: Built-in API docs endpoint

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (for WebSocket support)
- pip (Python package manager)

## ⚡ Quick Start

# 1. Clone and Setup

## Clone the repository
git clone <your-repo-url>
cd django-blog-backend

## Create virtual environment
python -m venv venv

# Activate virtual environment
### On Windows:
venv\Scripts\activate
### On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# 2. Environment Configuration

Create a `.env` file in the root directory:

SECRET_KEY=your-secret-key-here 
DEBUG=True
DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379


# 3. Database Setup


## Create PostgreSQL database
createdb blog_db

## Run migrations
python manage.py makemigrations
python manage.py migrate

## Create superuser
python manage.py createsuperuser


# 4. Start the Server

\`\`\`bash
## Start Django development server
python manage.py runserver

### The API will be available at: http://127.0.0.1:8000/api/


## 📚 API Documentation

### Base URL
\`\`\`
http://127.0.0.1:8000/api/
\`\`\`

### Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

\`\`\`
Authorization: Bearer <your-jwt-token>
\`\`\`

#### Get JWT Token

**Register a new user:**
```http
POST /api/auth/users/
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "role": "author"
}
