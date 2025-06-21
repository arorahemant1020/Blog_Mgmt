from django.contrib import admin
from django.urls import path, include
from blog.api_docs import api_documentation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/users/', include('users.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/docs/', api_documentation, name='api-docs'),
    path('', api_documentation, name='api-docs-root'),
]
