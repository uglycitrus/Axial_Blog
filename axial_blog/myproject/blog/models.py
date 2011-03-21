import datetime
import re

from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import defaultfilters


class Tag(models.Model):
	name = models.CharField(
		"Name",
		max_length = 50,
		unique = True,
		)
	slug = models.SlugField(
		"Slug",
		max_length = 50,
		unique = True,
		)
	created_date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		"""
		makes sure no blank names are saved to database
		makes sure all slugs are in fact slugs
		"""
		if len(self.name)<1: raise IntegrityError("Name must be at least 1 character")
		#elif re.match(r'^\W+$',self.name): raise IntegrityError("Name cannot be blank")
		else:
			if self.slug: self.slug = defaultfilters.slugify(self.slug)
			else: self.slug = defaultfilters.slugify(self.name)
			super(Tag, self).save(*args, **kwargs)

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
	body = models.TextField(
		)
	created_date = models.DateField(auto_now=True)
	edited_date = models.DateField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, verbose_name="tagged posts")

	def save(self, *args, **kwargs):
		"""
		prevents blank titles, slugs, and bodies from being saved
		makes sure all slugs are in fact slugs
		"""
		if len(self.title)<1 or len(self.slug)<1 or len(self.body)<1: raise IntegrityError("Title, Slug, and Body must be at least 1 character")
		#elif re.match(r'^\W+$',self.title) or re.match(r'^\W+$',self.slug) or re.match(r'^\W+$',self.body): raise IntegrityError("Title, Slug, and Body cannot be blank")
		else: 
			self.slug = defaultfilters.slugify(self.slug)
			super(BlogPost, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title

