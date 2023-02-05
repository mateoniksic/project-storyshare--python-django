from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.views.generic import TemplateView, ListView, DetailView


class IndexTemplateView(TemplateView):
    template_name = 'app/index/index.html'


class CreatorProfileListView(ListView):
    model = CreatorProfile
    context_object_name = 'creator_profiles'
    queryset = CreatorProfile.objects.all()
    template_name = 'app/creator_profile/creator_profile_list.html'


class CreatorProfileDetailView(DetailView):
    model = CreatorProfile
    context_object_name = 'creator_profile'
    template_name = 'app/creator_profile/creator_profile_detail.html'


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all()
    template_name = 'app/post/post_list.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post/post_detail.html'


class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'
    queryset = Tag.objects.all()
    template_name = 'app/tag/tag_list.html'


class TagDetailView(DetailView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'app/tag/tag_detail.html'
