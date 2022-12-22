"""
IMPORTS
"""
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.views.generic import TemplateView, ListView, DetailView

"""
INDEX VIEWS
"""
class IndexTemplateView(TemplateView):
	template_name = 'app/index/index.html'

"""
CREATOR PROFILE VIEWS
"""
class CreatorProfileListView(ListView):
	model = CreatorProfile
	template_name = 'app/creator_profile/creator_profile_list.html'
	context_object_name = 'creator_profiles'
	queryset = CreatorProfile.objects.all()

class CreatorProfileDetailView(DetailView):
	model = CreatorProfile
	context_object_name = 'creator_profile'
	template_name = 'app/creator_profile/creator_profile_detail.html'

"""
POST VIEWS
"""
class PostListView(ListView):
	model = Post
	template_name = 'app/post/post_list.html'
	context_object_name = 'posts'
	queryset = Post.objects.all()

class PostDetailView(DetailView):
	model = Post
	context_object_name = 'post'
	template_name = 'app/post/post_detail.html'

"""
TAG VIEWS
"""
class TagListView(ListView):
	model = Tag
	template_name = 'app/tag/tag_list.html'
	context_object_name = 'tags'
	queryset = Tag.objects.all()

class TagDetailView(DetailView):
	model = Tag
	context_object_name = 'tag'
	template_name = 'app/tag/tag_detail.html'