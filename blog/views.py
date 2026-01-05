from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from rest_framework import generics

from .models import Post, ContactMessage
from .serializers import PostSerializer, ContactMessageSerializer
from .forms import PostForm, UserRegisterForm

# -------- AUTH VIEWS --------

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'user_posts': user_posts,
        'post_count': user_posts.count(),
    }
    return render(request, 'blog/profile.html', context)

# -------- TEMPLATE VIEWS --------

def home(request):
    # OPEN ACCESS: Everyone sees the latest posts
    posts = Post.objects.filter(published=True).order_by('-created_at')[:6]
    return render(request, "blog/home.html", {"posts": posts})

def blog_list(request):
    # OPEN ACCESS: Everyone can browse the archive
    posts = Post.objects.filter(published=True).order_by('-created_at')
    return render(request, "blog/blog_list.html", {"posts": posts})

def blog_detail(request, slug):
    # OPEN ACCESS: Everyone can read stories
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, "blog/blog_detail.html", {"post": post})

@login_required(login_url='login')
def create_post(request):
    # RESTRICTED: Only logged-in users can write
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Generate unique slug
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
            
            post.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required(login_url='login')
def edit_post(request, slug):
    # Only the author can edit their post
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != request.user:
        return redirect('blog_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            
            # Update slug if title changed
            if post.title != updated_post.title:
                base_slug = slugify(updated_post.title)
                slug = base_slug
                counter = 1
                while Post.objects.filter(slug=slug).exclude(pk=post.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                updated_post.slug = slug
            
            updated_post.save()
            return redirect('blog_detail', slug=updated_post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required(login_url='login')
def delete_post(request, slug):
    # Only the author can delete their post
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != request.user:
        return redirect('blog_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        return redirect('profile')
    
    return render(request, 'blog/blog_detail.html', {'post': post})

def about(request):
    return render(request, "blog/about.html")

def contact(request):
    return render(request, "blog/contact.html")

# -------- API VIEWS --------

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    lookup_field = "slug"

class ContactCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer