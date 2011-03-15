import datetime

from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
	name = models.SlugField(
		max_length = "50",
		unique = True
		)
	created_date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class BlogPost(models.Model):
	"""
	Each BlogPost has a title, body, author, created date, edited date, and tags.
	The title and body are supplied by the user
	The author will be grabbed with request.user in the views layer
	created date and edited date will be assigned when in BlogPost.save()
	BlogPosts must have unique titles 
	"""
	title = models.CharField(
		"Title",
		max_length = 50,
		)
	slug = models.SlugField(
		"Slug", 
		max_length = 50,
		unique = True, 
		)
	author = models.ForeignKey(
		User, 
		verbose_name="Author",
		)
	body = models.TextField()
	created_date = models.DateField(auto_now=True)
	edited_date = models.DateField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, verbose_name="tagged posts")

	def __unicode__(self):
		return self.title

