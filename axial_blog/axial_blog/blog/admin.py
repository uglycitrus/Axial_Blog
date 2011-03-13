from axial_blog.blog.models import BlogPost
from axial_blog.blog.models import Tag

from django.contrib import admin

admin.site.register(BlogPost)
admin.site.register(Tag)
