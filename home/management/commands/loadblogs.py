import os

from django.conf import settings

BLOG_DIR = settings.BASE_DIR / "data" / "blogs"

for blog in os.listdir(BLOG_DIR):
    blog_file = BLOG_DIR / blog
    print(blog_file)
