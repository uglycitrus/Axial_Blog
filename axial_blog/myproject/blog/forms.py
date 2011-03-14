from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from myproject.blog.models import BlogPost
from myproject.blog.models import Tag

class LogInForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

class BlogPostForm(ModelForm):
	class Meta:
		model = BlogPost
		fields =  ('title', 'slug', 'body')

class PartialBlogPostForm(ModelForm):
	class Meta:
		model = BlogPost
		fields =  ('title', 'body')

class BlogPostSlugForm(forms.Form):
	slug = forms.SlugField(
		max_length = 50,
		label="Slug",
		)

class TagForm(forms.Form):
	name = forms.SlugField(
		max_length = 50,
		label="",
		)
