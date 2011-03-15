"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import unittest
import datetime

from datetime import timedelta

from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User

from myproject.blog.models import BlogPost
from myproject.blog.models import Tag

## class SimpleTest(TestCase):
##     def test_basic_addition(self):
##         """
##         Tests that 1 + 1 always equals 2.
##         """
##         self.failUnlessEqual(1 + 1, 2)
## 
## __test__ = {"doctest": """
## Another way to test that 1 + 1 is equal to 2.
## 
## >>> 1 + 1 == 2
## True
## """}


class BlogTest(unittest.TestCase):
	
	def setUp(self):
		self.user = User.objects.create(username = "user1")
		self.post1 = BlogPost.objects.create(title="This is Post#1", slug="post-1", body="woohoo yippee!",author=self.user)
		self.tag1 = Tag.objects.create(name="This-is-Tag#1")

	def SavePosts(self):
		"""
		Confirms that BlogPosts need unique slug, but all other fields can be identical
		Confirms that BlogPosts won't be saved w/o title, slug, body, and author
		!!! CANNOT FIGURE OUT HOW TO MAKE SURE ALL SLUGS SAVED IN THE DATABASE ARE SLUGS NOT CHARS!!!
		confirms we can't have multiple posts with the same title or tags with the same name
		"""
		try:
			(BlogPost.objects.create(title="This is Post#1", slug="post-1", body="woohoo yippee!",author=u))
			Cannot_save_post_with_same_name = False
		except:
			Cannot_save_post_with_same_name = True
		self.assertTrue(Cannot_save_post_with_same_name)
		self.assertEqual(BlogPost.objects.count(), 1)
		self.post2 = BlogPost.objects.create(title="This is Post#1", slug="1-post", body="woohoo yippee!",author=self.user)
		self.assertEqual(BlogPost.objects.count(), 2)

	def SaveTags(self):
		"""
		Confirms that Tags need unique names in slug form
		!!! CANNOT FIGURE OUT HOW TO MAKE SURE ALL SLUGS SAVED IN THE DATABASE ARE SLUGS NOT CHARS!!!
		"""
		self.assertEqual(Tag.objects.count(), 1)
		try:
			Tag.objects.create(name="This-is-Tag#1")
			Cannot_save_tag_with_same_name = False
		except:
			Cannot_save_tag_with_same_name = True
		self.assertTrue(Cannot_save_tag_with_same_name)
		self.tag2 = Tag.objects.create(name="This-is-Tag#2")
		self.assertTrue(self.tag2)
		self.assertEqual(Tag.objects.count(), 2)

	def AddTags(self):
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

	def Posts(self):
		c = Client()
		response = c.get('/posts/')
		self.assertEqual(response.status_code, 200)
	
	def PostsView(self):
		c = Client()
		self.assertRaises("TemplateDoesNotExist: 404.html", c.get('/posts/non-existent-post'))
