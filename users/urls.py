from django.urls import path
from . import views

urlpatterns = [
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),
    
    # User listings
    path('', views.UserListView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('authors/', views.authors_list, name='authors-list'),
    
    # Statistics
    path('stats/', views.user_stats, name='user-stats'),
]
