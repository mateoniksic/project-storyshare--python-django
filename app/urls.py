"""
IMPORTS
"""
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
	path('', views.IndexTemplateView.as_view(), name = 'index'),
	path('creators/', views.CreatorProfileListView.as_view(), name = 'creator-profile-list-view'),
	path('creators/<slug:slug>/', views.CreatorProfileDetailView.as_view(), name = 'creator-profile-detail-view'),
	path('posts/', views.PostListView.as_view(), name = 'post-list-view'),
	path('posts/<slug:slug>/', views.PostDetailView.as_view(), name = 'post-detail-view'),
	path('tags/', views.TagListView.as_view(), name = 'tag-list-view'),
	path('tags/<slug:slug>/', views.TagDetailView.as_view(), name = 'tag-detail-view'),
]