"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import unittest
import datetime

from datetime import timedelta

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
	def setUP(self):
		"""
		confirms we can't have multiple posts with the same title or tags with the same name
		"""
		u = User.objects.all()[0]
		self.post1 = BlogPost.objects.create(title="This is Post#1",body="woohoo yippee!",author=u)
		self.post2 = BlogPost.objects.create(title="This is Post#2",body="woohoo yippee!",author=u)
		self.post3 = BlogPost.objects.create(title="This is Post#2",body="woohoo yippee!",author=u)
		self.tag1 = Tag.objects.create(name="This is Tag#1")
		self.tag2 = Tag.objects.create(name="This is Tag#2")
		self.tag3 = Tag.objects.create(name="This is Tag#2")
		self.assertEqual(BlogPost.objects.count(), 2)
		self.assertEqual(Tag.objects.count(), 2)

	def testDates(self):
		"""
		confirms that created dates are actually today, and edited dates are independent of created dates
		"""
		u = User.objects.all()[0]
		self.post4 = BlogPost.objects.create(title="This is Post#4",body="woohoo yippee!",author=u) #create post
		self.assertEqual(self.post1.created_date, datetime.date.today())
		self.post1.created_date = self.post1.created_date - timedelta(days = 1)  #set created date to yesterday
		self.post1.save() #save it
		self.post1.save() #save it with custom save function to make sure created date isn't overwritten
		self.assertEqual(self.post1.edited_date, datetime.date.today())
		self.assertEqual(self.post1.created_date, datetime.date.today() - timedelta(days = 1))
		self.tag1 = Tag.objects.create(name="This is Tag#1")
		self.assertEqual(self.tag1.created_date, datetime.date.today())

	def testAddTags(self):
		u = User.objects.all()[0]
		self.post1 = BlogPost.objects.create(title="This is Post#1",body="woohoo yippee!",author=u)
		self.post2 = BlogPost.objects.create(title="This is Post#2",body="woohoo yippee!",author=u)
		self.tag1 = Tag.objects.create(name="This is Tag#1")
		self.tag2 = Tag.objects.create(name="This is Tag#2")
		self.tag3 = Tag.objects.create(name="This is Tag#3")
		self.tag3.posts.add(self.post1)
		self.tag3.posts.add(self.post2)
		self.assertEqual(self.tag3.posts.count(), 2)
