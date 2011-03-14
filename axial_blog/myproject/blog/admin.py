from myproject.blog.models import BlogPost
from myproject.blog.models import Tag

from django.contrib import admin

admin.site.register(BlogPost)
admin.site.register(Tag)
