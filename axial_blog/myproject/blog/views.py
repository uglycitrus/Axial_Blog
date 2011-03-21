from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from myproject.blog.models import BlogPost
from myproject.blog.models import Tag

from myproject.blog.forms import LogInForm
from myproject.blog.forms import BlogPostSlugForm
from myproject.blog.forms import PartialBlogPostForm
from myproject.blog.forms import BlogPostForm
from myproject.blog.forms import TagForm

def login_view(request):
	next = request.GET.get('next')
	# forward the user to the list of posts to edit if they are logged in
	if request.user.is_authenticated():
		return HttpResponseRedirect( reverse('edit_posts') )
	# if they're not logged in already they must complete the sign in form
	form = LogInForm()
	if request.method == 'POST':
		form = LogInForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')
			try: user = authenticate(username = username, password = password)
			except: return render_to_response('login.html', {'form':form, 'user':user, 'error':'user does not exist'})
			try:
				if user.is_active:
					login(request, user)	
					if next: return HttpResponseRedirect(next) 
					else: return HttpResponseRedirect(reverse('edit_posts'))
			except: return render_to_response('login.html', {'form':form, 'user':user, 'error':'user is not active'})
	return render_to_response('login.html', {'form':form})


def logout_view(request):
	logout(request)
	return HttpResponseRedirect( reverse('all_posts'))

@login_required
def new_post(request):
	TagFormSet = formset_factory(TagForm)
	tag_formset = TagFormSet()
	blogpost_form = BlogPostForm()
	if request.method == 'POST':
		blogpost_form = BlogPostForm(request.POST)
		tag_formset = TagFormSet(request.POST)
		if blogpost_form.is_valid() and tag_formset.is_valid():
			post = BlogPost()
			post.title = blogpost_form.cleaned_data['title']
			post.slug = blogpost_form.cleaned_data['slug']
			post.body = blogpost_form.cleaned_data['body']
			post.author = request.user
			post.save()
			for i in tag_formset.cleaned_data:
				tag = Tag()
				tag.name = i['name']
				tag, created = Tag.objects.get_or_create(name = tag.name) 
				post.tags.add(tag)
			return HttpResponseRedirect(reverse('edit_posts'))
	return render_to_response('post_edit.html',{'form':blogpost_form,'formset':tag_formset})

@login_required
def post_edit(request, post_slug):
	"""
	Edit individual blog post titles, slugs, bodies and tags
	"""
	#if the url does not lead us to a blogpost to edit, then 404
	post = get_object_or_404(BlogPost, slug = post_slug)
	tags = post.tags.all()
	TagFormSet = formset_factory(TagForm, extra=0)
	#initialize partial blogpost form
	blogpost_form = PartialBlogPostForm(initial={
		'title' : post.title,
		'body' : post.body,
		})
	#initialize separate slug form so that slug can be edited
	slug_form = BlogPostSlugForm(initial={
		'slug':post.slug,
		})
	#initialize tag formset
	initial=[]
	[initial.append({'name':i.name}) for i in tags]
	tag_formset = TagFormSet(initial = initial)
	if request.method == 'POST':
		blogpost_form = PartialBlogPostForm(request.POST)
		tag_formset = TagFormSet(request.POST)
		slug_form = BlogPostSlugForm(request.POST)
		if blogpost_form.is_valid() and tag_formset.is_valid() and slug_form.is_valid():
			#if the edited post's slug has been changed make sure it's doesn't conflict with other posts' slug fields
			if post.slug != slug_form.cleaned_data['slug']:
				try:
					post = BlogPost.objects.get(slug = slug_form.cleaned_data['slug'])
					error = 'BlogPost with this slug already exists'
					return render_to_response('post_edit.html',{'form':blogpost_form,'formset':tag_formset,'slug_form':slug_form,'error':error})
				except:
					post.slug = slug_form.cleaned_data['slug']
			post.title = blogpost_form.cleaned_data['title']
			post.body = blogpost_form.cleaned_data['body']
			post.save()
			#the newly submited tags must be handled so that 1)Tag objects are created if necessary 2)Tags are added and Removed from the edited post based on new tags
			new_tags = []
			for i in tag_formset.cleaned_data:
				tag = Tag()
				tag.name = i['name']
				tag, created = Tag.objects.get_or_create(name = tag.name) 
				new_tags.append(tag)
				post.tags.add(tag)
			for tag in tags:
				if tag not in new_tags:
					post.tags.remove(tag)	
			return HttpResponseRedirect(reverse('edit_posts'))
	return render_to_response('post_edit.html',{'form':blogpost_form,'formset':tag_formset,'slug_form':slug_form})

@login_required
def edit_posts(request):
	posts = BlogPost.objects.all()
	return render_to_response('edit_posts.html',{'posts':posts})

def post_list(request, tag_slug):
	tags = get_object_or_404(Tag, slug = tag_slug)
	posts = tags.blogpost_set.all()
	return render_to_response('posts.html',{'posts':posts})

def all_posts(request):
	posts = BlogPost.objects.all()
	return render_to_response('posts.html',{'posts':posts})

def post_view(request, post_slug):
	post = get_object_or_404(BlogPost, slug = post_slug)
	tags = post.tags.all()
	return render_to_response('post_view.html',{'post':post,'tags':tags})

def all_posts(request):
	posts = BlogPost.objects.all()
	return render_to_response('posts.html',{'posts':posts})
