from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Core
    path('', views.home, name='home'),
    path('stories/', views.blog_list, name='blog_list'),
    path('stories/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('write/', views.create_post, name='create_post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    
    # The New Profile Page
    path('profile/', views.profile, name='profile'),
    
    # Static
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Auth
    path('register/', views.register, name='register'),
    # We use next_page='profile' to force redirect to profile after login
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html', next_page='profile'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # API
    path('api/posts/', views.PostListAPIView.as_view(), name='api_post_list'),
    path('api/posts/<slug:slug>/', views.PostDetailAPIView.as_view(), name='api_post_detail'),
    path('api/contact/', views.ContactCreateAPIView.as_view(), name='api_contact_create'),
]