from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index-template-view'),

    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),

    path('for-you/', views.ForYouPostListView.as_view(), name='for-you-post-list-view'),
    path('following/', views.FollowingPostListView.as_view(), name='following-post-list-view'),

    path('post/create', views.PostCreateView.as_view(), name='post-create-view'),
    path('post/<slug:slug>/update', views.PostUpdateView.as_view(), name='post-update-view'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail-view'),
    path('post/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post-delete-view'),

    path('profile/<slug:slug>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),
    path('profile/<slug:slug>/update/', views.ProfileUpdateView.as_view(), name='profile-update-view'),

    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag-detail-view'),

    path('search/member/', views.SearchMemberListView.as_view(), name='search-member-list-view'),
]
