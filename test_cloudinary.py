import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innerpieces.settings')
django.setup()

from django.conf import settings
from blog.models import Post

print("=" * 50)
print("CLOUDINARY CONFIGURATION TEST")
print("=" * 50)

print(f"\nDEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")

if hasattr(settings, 'CLOUDINARY_STORAGE'):
    print(f"\nCLOUDINARY_STORAGE:")
    for key, value in settings.CLOUDINARY_STORAGE.items():
        if 'SECRET' in key:
            print(f"  {key}: {'*' * 10}")
        else:
            print(f"  {key}: {value}")
else:
    print("\nCLOUDINARY_STORAGE: Not configured")

print(f"\nCLOUDINARY_URL env: {'Set' if os.environ.get('CLOUDINARY_URL') else 'Not set'}")

posts = Post.objects.all()
print(f"\n\nPOSTS IN DATABASE: {posts.count()}")
for post in posts:
    print(f"\nPost: {post.title}")
    print(f"  Has image: {bool(post.image)}")
    if post.image:
        print(f"  Image field: {post.image.name}")
        print(f"  Image URL: {post.image.url}")
