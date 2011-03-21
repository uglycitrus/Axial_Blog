"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import unittest
import datetime
import re

from datetime import timedelta

from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import defaultfilters

from myproject.blog.models import BlogPost
from myproject.blog.models import Tag


class BlogTest(unittest.TestCase):
	
	def setUp(self):
		self.user = User.objects.create(username = "user1")
		self.user.set_password('user1')
		self.user.save()
		self.post1 = BlogPost.objects.create(title="This is Post#1", slug="post-1", body="woohoo yippee!",author=self.user)
		self.tag1 = Tag.objects.create(name="This is Tag#1")

	def SavePosts(self):
		"""
		Confirms that BlogPosts need unique slug, but all other fields can be identical
		Confirms that BlogPosts won't be saved w/o title, slug, body, and author
		"""
		#non-unique slug
		self.assertRaises(IntegrityError, lambda : BlogPost.objects.create(title="This is a new title", slug="post-1", body="Brand new body!",author=self.user))
		self.assertEqual(BlogPost.objects.count(), 1)
		#unique slug
		self.post2 = BlogPost.objects.create(title="This is Post#1", slug="1-post", body="woohoo yippee!",author=self.user)
		self.assertEqual(BlogPost.objects.count(), 2)
		#no title
		self.assertRaises(IntegrityError, lambda : BlogPost.objects.create(slug="no-title-slug", body="New slug, and new body, w/o a title!",author=self.user))
		#no slug
		self.assertRaises(IntegrityError, lambda : BlogPost.objects.create(title="This is a new title, but it has no slug", body="This is a new body, but it has no slug.  woohoo yippee!",author=self.user))
		#no body
		self.assertRaises(IntegrityError, lambda : BlogPost.objects.create(title="This is Post has no body", slug="no-body-slug", author=self.user))
		#no author
		self.assertRaises(IntegrityError, lambda : BlogPost.objects.create(title="This is Post has no author", slug="no-author-slug", body="This is a new body, but it has no author.  woohoo yippee!"))


	def UnicodePosts(self):
		"""
		Confirms that unicode output for posts will be the title
		"""
		#basic title
		self.post2 = BlogPost.objects.create(title="This is Post#2", slug="2-post", body="woohoo yippee!",author=self.user)
		self.assertEqual(self.post2.__unicode__(), self.post2.title)
		#bunch of random characters for a title
		self.post2 = BlogPost.objects.create(title="~`!@#$%^&*()_-+=|}{[]:;?><,./1234567890\"", slug="3-post", body="woohoo yippee!",author=self.user)
		self.assertEqual(self.post2.__unicode__(), self.post2.title)

	def SaveTags(self):
		"""
		Confirms that Tags need unique names 
		Confirmst that Tag slugs are in fact slugs
		"""
		self.assertEqual(Tag.objects.count(), 1)
		#non-unique name
		self.assertRaises(IntegrityError, lambda: Tag.objects.create(name="This is Tag#1"))
		#non-unique slug
		self.assertRaises(IntegrityError, lambda: Tag.objects.create(name="This is Tag#2", slug="This-is-Tag#1"))
		#name full of spaces
		self.assertRaises(IntegrityError, lambda: Tag.objects.create(name="       "))
		#unique name
		self.tag2 = Tag.objects.create(name="This is Tag#2")
		self.assertEqual(self.tag2.slug, defaultfilters.slugify("This is Tag#2"))
		self.assertEqual(Tag.objects.count(), 2)
		#unique name full of random characters
		name = "~`!@#$%^&*()_-+=|}{[]:;?><,./1234567890"
		self.tag2 = Tag.objects.create(name=name)
		self.assertEqual(self.tag2.slug, defaultfilters.slugify(name))
		self.assertEqual(Tag.objects.count(), 3)

	def UnicodeTags(self):
		"""
		Confirms that unicode output for posts will be the title
		"""
		#basic title
		self.tag2 = Tag.objects.create(name="This is tag#2")
		self.assertEqual(self.tag2.__unicode__(), self.tag2.name)
		#bunch of random characters for a name
		self.tag2 = Tag.objects.create(name="~`!@#$%^&*()_-+=|}{[]:;?><,./1234567890\"")
		self.assertEqual(self.tag2.__unicode__(), self.tag2.name)
		

	def TagPosts(self):
		"""
		confirms that the same tag cannot be added to a post multiple times, but multiple different tags can
		"""
		self.tag2 = Tag.objects.create(name="This-is-Tag#2")
		self.tag3 = Tag.objects.create(name="This-is-Tag#3")
		self.post2 = BlogPost.objects.create(title="This is Post#2", slug="post-2", body="woohoo yippee!",author=self.user)
		self.post3 = BlogPost.objects.create(title="This is Post#3", slug="post-3", body="woohoo yippee!",author=self.user)
		self.post3.tags.add(self.tag2)
		self.post3.tags.add(self.tag3)
		self.assertEqual(self.post3.tags.count(), 2)
		self.post3.tags.add(self.tag3)
		self.assertEqual(self.post3.tags.count(), 2)

	def PostsList(self):
		c = Client()
		response = c.get('/posts/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/posts/this-is-tag1')
		self.assertEqual(response.status_code, 200)
	
	def Login(self):
		"""
		Confirms that if logged in client status is 302s
		And that if not logged in, runs smooth
		"""
		c = Client()
		#200 when not signed in
		response = c.get('/accounts/login/')
		self.assertEqual(response.status_code, 200)
		#302 when signed in
		self.assertTrue(c.login(username='user1', password='user1'))
		response = c.get('/accounts/login/')
		self.assertEqual(response.status_code, 302)
		#Login Form Posts properly
		c.logout()
		response = c.post('/accounts/login/', {'username':'user1','password':'user1'})
		self.assertEqual(response.status_code, 302)

	def Logout(self):
		"""
		Confirms client status is 302s whether logged in or not
		"""
		c = Client()
		response = c.get('/accounts/logout/')
		self.assertEqual(response.status_code, 302)
		self.assertTrue(c.login(username='user1', password='user1'))
		response = c.get('/accounts/logout/')
		self.assertEqual(response.status_code, 302)

	def PostsEditList(self):
		"""
		Confirms that if not logged in client status is 302s
		And that if logged in, runs smooth
		"""
		c = Client()
		#302 when not signed in
		response = c.get('/posts/edit/')
		self.assertEqual(response.status_code, 302)
		#200 when signed in
		self.assertTrue(c.login(username='user1', password='user1'))
		response = c.get('/posts/edit/')
		self.assertEqual(response.status_code, 200)

	def PostsNew(self):
		"""
		Confirms that if not logged in client status is 302s
		And that if logged in, runs smooth
		Once confirmed in tags and posts can be added
		"""
		c = Client()
		#302 when not signed in
		response = c.get('/posts/new/')
		self.assertEqual(response.status_code, 302)
		#200 when signed in
		self.assertTrue(c.login(username='user1', password='user1'))
		response = c.get('/posts/new/')
		self.assertEqual(response.status_code, 200)
		#successfully posts forms
		response = c.post('/posts/new/', {
			'title': u'New Post', 
			'slug': u'new-slug', 
			'body': u'new body', 
			'form-TOTAL_FORMS': u'1',
			'form-INITIAL_FORMS': u'0',
			'form-MAX_NUM_FORMS': u'',
			'form-0-name': u'new tag'
			})
		self.assertEqual(BlogPost.objects.count(), 2)
		self.assertEqual(Tag.objects.count(), 2)
		self.assertEqual(BlogPost.objects.all()[1].title, 'New Post')
		self.assertEqual(BlogPost.objects.all()[1].tags.count(), 1)
		self.assertEqual(Tag.objects.all()[1].name, 'new tag')

	def PostsView(self):
		"""
		Confirmst that non existent slugs raise 404s
		But existent slugs don't 404 even if they're random symbols and numbers
		"""
		c = Client()
		response = c.get('/posts/view/non-existent-blog-post')
		self.assertEqual(response.status_code, 404)
		#post with random number and symbol slug
		self.post2 = BlogPost.objects.create(title="~`!@#$%^&*()_-+=|}{[]:;?><,./1234567890\"", slug="3-post", body="woohoo yippee!",author=self.user)
		response2 = c.get('/posts/view/'+self.post2.slug)
		self.assertEqual(response2.status_code, 200)
		#post with normal slug
		response3 = c.get('/posts/view/'+self.post1.slug)
		self.assertEqual(response3.status_code, 200)

	def PostsEdit(self):
		"""
		Confirms that if not logged in client status is 302s
		Once logged in:
			Confirmst that non existent slugs raise 404s
			But existent slugs don't 404 even if they're random symbols and numbers
		"""
		c = Client()
		response = c.get('/posts/edit/'+self.post1.slug)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(c.login(username='user1', password='user1'))
		response = c.get('/posts/edit/non-existent-blog-post')
		self.assertEqual(response.status_code, 404)
		#post with random number and symbol slug
		self.post2 = BlogPost.objects.create(title="~`!@#$%^&*()_-+=|}{[]:;?><,./1234567890\"", slug="3-post", body="woohoo yippee!",author=self.user)
		response2 = c.get('/posts/edit/'+self.post2.slug)
		self.assertEqual(response2.status_code, 200)
		#post with normal slug
		response3 = c.get('/posts/edit/'+self.post1.slug)
		self.assertEqual(response3.status_code, 200)
		#successfully posts forms
		response = c.post('/posts/edit/'+self.post1.slug, {
			'title': u'New Post', 
			'slug': u'new-slug', 
			'body': u'new body', 
			'form-TOTAL_FORMS': u'2',
			'form-INITIAL_FORMS': u'0',
			'form-MAX_NUM_FORMS': u'',
			'form-0-name': u'new tag',
			'form-1-name': u'This is Tag#1'
			})
		self.post1 = BlogPost.objects.get(title="New Post")
		self.assertEqual(BlogPost.objects.count(), 2)
		self.assertEqual(Tag.objects.count(), 2)
		self.assertEqual(self.post1.title, 'New Post')
		self.assertEqual(self.post1.tags.count(), 2)
		self.assertEqual(Tag.objects.all()[1].name, 'new tag')
		response = c.post('/posts/edit/'+self.post1.slug, {
			'title': u'New Post', 
			'slug': u'new-slug', 
			'body': u'new body', 
			'form-TOTAL_FORMS': u'2',
			'form-INITIAL_FORMS': u'2',
			'form-MAX_NUM_FORMS': u'',
			'form-0-name': u'new tag',
			'form-1-name': u'newer tag'
			})
		self.post1 = BlogPost.objects.get(title="New Post")
		self.assertEqual(BlogPost.objects.count(), 2)
		self.assertEqual(Tag.objects.count(), 3)
		self.assertEqual(self.post1.title, 'New Post')
		self.assertEqual(self.post1.tags.all()[1].name, 'newer tag')
		#form errors
		response = c.post('/posts/edit/'+self.post1.slug, {
			'title': u'', 
			'slug': u'', 
			'body': u'', 
			'form-TOTAL_FORMS': u'1',
			'form-INITIAL_FORMS': u'0',
			'form-MAX_NUM_FORMS': u'',
			'form-0-name': u'',
			})
		
